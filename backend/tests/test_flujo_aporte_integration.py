"""
Tests de integración para el flujo de Aporte y Validación de Cursos (API HTTP + DB real en memoria).
Verifica:
1. Permisos: autor sin sesión -> 401
2. Aporte válido -> creado en estado PENDING (en_revision)
3. Permisos: moderador sin rol -> 403
4. Validar aprobado -> pasa a PUBLISHED y aparece en GET /cursos
5. Validar rechazado -> pasa a REJECTED y NO aparece en GET /cursos
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db

@pytest.fixture
def client():
    # Setup de base de datos aislada en memoria con StaticPool para compartir conexión
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_flujo_aporte_autor_sin_sesion_retorna_401(client):
    # Arrange: payload de aporte sin enviar cabecera Authorization
    payload = {
        "title": "Arquitectura Hexagonal con Python",
        "url": "https://cursoteca.org/hexagonal",
        "platform": "YouTube",
        "technology": "Python",
        "level": "Avanzado"
    }

    # Act
    response = client.post("/api/aportes", json=payload)

    # Assert
    assert response.status_code == 401
    assert "Autor sin sesión" in response.json()["detail"]


def test_flujo_aporte_valido_con_sesion_crea_curso_en_estado_en_revision(client):
    # Arrange: aporte válido con cabecera de sesión
    headers = {"Authorization": "Bearer token_usuario_activo"}
    payload = {
        "title": "FastAPI Microservicios y Docker",
        "url": "https://cursoteca.org/fastapi-micro",
        "platform": "Udemy",
        "technology": "FastAPI",
        "level": "Intermedio"
    }

    # Act
    response = client.post("/api/aportes", json=payload, headers=headers)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PENDING"
    assert data["title"] == "FastAPI Microservicios y Docker"
    assert "id" in data


def test_flujo_aporte_moderar_validador_sin_rol_retorna_403(client):
    # Arrange: crear un aporte previamente con usuario normal
    headers_user = {"Authorization": "Bearer user_token"}
    aporte_res = client.post("/api/aportes", json={
        "title": "Curso Kubernetes Práctico",
        "url": "https://cursoteca.org/k8s-practico",
        "platform": "YouTube",
        "technology": "DevOps",
        "level": "Principiante"
    }, headers=headers_user)
    curso_id = aporte_res.json()["id"]

    # Act: usuario intenta moderar sin enviar X-User-Role MODERATOR (o con rol USER)
    headers_no_mod = {"X-User-Role": "USER"}
    mod_res = client.post(f"/api/aportes/{curso_id}/moderar", json={"decision": "APPROVED"}, headers=headers_no_mod)

    # Assert
    assert mod_res.status_code == 403
    assert "MODERATOR" in mod_res.json()["detail"]


def test_flujo_aporte_validar_aprobado_curso_publicado_y_visible_en_catalogo(client):
    # Arrange: crear un aporte en estado PENDING
    headers_user = {"Authorization": "Bearer user_token"}
    aporte_res = client.post("/api/aportes", json={
        "title": "Mastering Go & Concurrency",
        "url": "https://cursoteca.org/golang-concurrency",
        "platform": "Web",
        "technology": "Go",
        "level": "Avanzado"
    }, headers=headers_user)
    curso_id = aporte_res.json()["id"]

    # Act: moderador aprueba el curso
    headers_mod = {"X-User-Role": "MODERATOR"}
    mod_res = client.post(f"/api/aportes/{curso_id}/moderar", json={"decision": "APPROVED"}, headers=headers_mod)
    assert mod_res.status_code == 200
    assert mod_res.json()["status"] == "PUBLISHED"

    # Act 2: consultar catálogo público
    catalogo_res = client.get("/api/cursos")

    # Assert
    assert catalogo_res.status_code == 200
    cursos_catalogo = catalogo_res.json()
    ids_en_catalogo = [c["id"] for c in cursos_catalogo]
    assert curso_id in ids_en_catalogo


def test_flujo_aporte_validar_rechazado_no_visible_en_catalogo(client):
    # Arrange: crear un aporte en estado PENDING
    headers_user = {"Authorization": "Bearer user_token"}
    aporte_res = client.post("/api/aportes", json={
        "title": "Tutorial HTML Obsolescente 2005",
        "url": "https://cursoteca.org/html-old",
        "platform": "Blog",
        "technology": "HTML",
        "level": "Principiante"
    }, headers=headers_user)
    curso_id = aporte_res.json()["id"]

    # Act: moderador rechaza el curso indicando motivo
    headers_mod = {"X-User-Role": "MODERATOR"}
    mod_res = client.post(
        f"/api/aportes/{curso_id}/moderar",
        json={"decision": "REJECTED", "rejection_reason": "El contenido está desactualizado y no cumple el estándar mínimo."},
        headers=headers_mod
    )
    assert mod_res.status_code == 200
    assert mod_res.json()["status"] == "REJECTED"

    # Act 2: consultar catálogo público
    catalogo_res = client.get("/api/cursos")

    # Assert: el curso rechazado NO debe figurar en el catálogo público
    assert catalogo_res.status_code == 200
    cursos_catalogo = catalogo_res.json()
    ids_en_catalogo = [c["id"] for c in cursos_catalogo]
    assert curso_id not in ids_en_catalogo
