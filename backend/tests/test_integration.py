"""
Tests de integración para CursoRepository con base de datos real (SQLite en memoria).

Justificación de la elección de persistencia:
Se utiliza SQLite en memoria (`sqlite:///:memory:`) para la suite de integración de repositorios.
Esta elección provee:
1. Hermetismo total: cada test corre con un esquema limpio creado desde cero en memoria, garantizando aislamiento sin efectos secundarios.
2. Velocidad y reproducibilidad: no requiere servicios externos ni red ni tiempos de espera de contenedor, permitiendo feedback inmediato en local y CI.
3. Compatibilidad declarativa: utiliza los mismos modelos declarativos SQLAlchemy 2.0 y el mismo SQL relacional que PostgreSQL en producción.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.cursos.models import Category, Course
from app.cursos.repository import CursoRepository

@pytest.fixture
def db_session():
    # Arrange: crear motor SQLite en memoria y tablas limpias por test
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    # Sembrar categorías iniciales de prueba
    cat_backend = Category(id=1, name="Backend", slug="backend")
    cat_devops = Category(id=2, name="DevOps", slug="devops")
    session.add_all([cat_backend, cat_devops])
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


def test_curso_repository_create_and_get_by_id_roundtrip_exitoso(db_session):
    # Arrange
    repo = CursoRepository(db_session)
    nuevo_curso_data = {
        "title": "Arquitectura Limpia con FastAPI",
        "canonical_url": "https://cursoteca.org/fastapi-clean",
        "technology": "Python",
        "platform": "YouTube",
        "level": "Avanzado",
        "category_id": 1,
        "status": "PUBLISHED"
    }

    # Act
    curso_creado = repo.create(nuevo_curso_data)
    curso_recuperado = repo.get_by_id(curso_creado.id)

    # Assert
    assert curso_recuperado is not None
    assert curso_recuperado.id == curso_creado.id
    assert curso_recuperado.title == "Arquitectura Limpia con FastAPI"
    assert curso_recuperado.technology == "Python"
    assert curso_recuperado.status == "PUBLISHED"


def test_curso_repository_list_paginated_dos_paginas_conteo_correcto(db_session):
    # Arrange
    repo = CursoRepository(db_session)
    for i in range(1, 4):  # Crear 3 cursos
        repo.create({
            "title": f"Curso Docker Parte {i}",
            "canonical_url": f"https://cursoteca.org/docker-{i}",
            "technology": "DevOps",
            "platform": "YouTube",
            "category_id": 2,
            "status": "PUBLISHED"
        })

    # Act: página 1 con size 2 -> debe traer 2 cursos
    items_p1, total_count = repo.list_paginated(page=1, size=2)
    # Act: página 2 con size 2 -> debe traer el 1 curso restante
    items_p2, _ = repo.list_paginated(page=2, size=2)

    # Assert
    assert total_count == 3
    assert len(items_p1) == 2
    assert len(items_p2) == 1
    # Asegurar que no hay solapamiento entre páginas
    ids_p1 = {c.id for c in items_p1}
    ids_p2 = {c.id for c in items_p2}
    assert ids_p1.isdisjoint(ids_p2)


def test_curso_repository_filtro_busqueda_q_parcial_case_insensitive_exitoso(db_session):
    # Arrange
    repo = CursoRepository(db_session)
    repo.create({
        "title": "Aprende REACT desde Cero",
        "canonical_url": "https://cursoteca.org/react-zero",
        "technology": "Frontend",
        "platform": "Web",
        "status": "PUBLISHED"
    })
    repo.create({
        "title": "Bases de Datos con PostgreSQL",
        "canonical_url": "https://cursoteca.org/postgres",
        "technology": "Databases",
        "platform": "Udemy",
        "status": "PUBLISHED"
    })

    # Act: buscar 'react' en minúscula debe encontrar 'Aprende REACT desde Cero'
    items, total = repo.list_paginated(page=1, size=10, q="react")

    # Assert
    assert total == 1
    assert len(items) == 1
    assert "REACT" in items[0].title


def test_curso_repository_filtro_por_categoria_exitoso(db_session):
    # Arrange
    repo = CursoRepository(db_session)
    repo.create({
        "title": "FastAPI Masterclass",
        "canonical_url": "https://cursoteca.org/fastapi",
        "technology": "Python",
        "platform": "YouTube",
        "category_id": 1,  # Backend
        "status": "PUBLISHED"
    })
    repo.create({
        "title": "Kubernetes en Producción",
        "canonical_url": "https://cursoteca.org/k8s",
        "technology": "DevOps",
        "platform": "YouTube",
        "category_id": 2,  # DevOps
        "status": "PUBLISHED"
    })

    # Act: filtrar por category_id=1
    items, total = repo.list_paginated(page=1, size=10, category_id=1)

    # Assert
    assert total == 1
    assert len(items) == 1
    assert items[0].title == "FastAPI Masterclass"
    assert items[0].category_id == 1


def test_curso_repository_update_campos_parciales_exitoso(db_session):
    # Arrange
    repo = CursoRepository(db_session)
    curso = repo.create({
        "title": "Python para Principiantes",
        "canonical_url": "https://cursoteca.org/python-init",
        "technology": "Python",
        "platform": "YouTube",
        "level": "Principiante",
        "status": "PENDING"
    })

    # Act: actualizar título y nivel parcialmente
    curso_actualizado = repo.update(curso.id, {"title": "Python 3 Moderno", "level": "Intermedio"})

    # Assert
    assert curso_actualizado is not None
    assert curso_actualizado.title == "Python 3 Moderno"
    assert curso_actualizado.level == "Intermedio"
    # Campos no modificados deben permanecer intactos
    assert curso_actualizado.platform == "YouTube"
    assert curso_actualizado.status == "PENDING"


def test_curso_repository_delete_y_get_by_id_retorna_none(db_session):
    # Arrange
    repo = CursoRepository(db_session)
    curso = repo.create({
        "title": "Curso a Eliminar",
        "canonical_url": "https://cursoteca.org/temp",
        "technology": "General",
        "platform": "Web",
        "status": "PENDING"
    })
    curso_id = curso.id

    # Act
    fue_eliminado = repo.delete(curso_id)
    curso_despues_de_borrar = repo.get_by_id(curso_id)

    # Assert
    assert fue_eliminado is True
    assert curso_despues_de_borrar is None
