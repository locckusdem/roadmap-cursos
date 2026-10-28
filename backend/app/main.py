from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app.cursos.models import Course, Category
from app.cursos.repository import CursoRepository
from app.cursos.rules import validar_aporte_curso, DomainValidationError
from app.aportes.rules import (
    validar_permisos_moderacion,
    validar_decision_moderacion,
    AportePermissionError,
    AporteStateError,
    AporteValidationError
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    # Sembrar cursos iniciales si está vacío
    db = next(get_db())
    try:
        if db.query(Course).count() == 0:
            c1 = Course(
                id="1",
                title="Introducción a Docker y Contenedores",
                canonical_url="https://youtube.com/watch?v=docker-intro",
                platform="YouTube",
                technology="DevOps",
                level="Principiante",
                status="PUBLISHED"
            )
            c2 = Course(
                id="2",
                title="FastAPI y Arquitectura Limpia",
                canonical_url="https://cursoteca.org/fastapi-clean",
                platform="Web",
                technology="Python",
                level="Intermedio",
                status="PUBLISHED"
            )
            db.add_all([c1, c2])
            db.commit()
    finally:
        db.close()
    yield

app = FastAPI(title="Roadmap Cursos API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AporteCreateSchema(BaseModel):
    title: str = Field(..., min_length=5)
    url: str
    platform: str
    technology: str
    level: str = "Principiante"
    edition_year: Optional[int] = None

class ModerarPayloadSchema(BaseModel):
    decision: str  # APPROVED | REJECTED
    rejection_reason: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cursos")
@app.get("/api/cursos")
def get_cursos(
    page: int = 1,
    size: int = 20,
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    repo = CursoRepository(db)
    items, total = repo.list_paginated(page=page, size=size, q=q, category_id=category_id, status="PUBLISHED")
    return [
        {
            "id": c.id,
            "title": c.title,
            "canonical_url": c.canonical_url,
            "platform": c.platform,
            "technology": c.technology,
            "level": c.level,
            "status": c.status
        }
        for c in items
    ]

@app.post("/aportes", status_code=status.HTTP_201_CREATED)
@app.post("/api/aportes", status_code=status.HTTP_201_CREATED)
def crear_aporte(
    payload: AporteCreateSchema,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    # Validar sesión: autor sin sesión -> 401
    if not authorization or not authorization.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autor sin sesión: se requiere autenticación para postular un curso."
        )

    # Validar reglas de dominio de aporte
    try:
        validar_aporte_curso(payload.model_dump())
    except DomainValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    repo = CursoRepository(db)
    nuevo_curso = repo.create({
        "title": payload.title,
        "canonical_url": payload.url,
        "platform": payload.platform,
        "technology": payload.technology,
        "level": payload.level,
        "status": "PENDING"
    })

    return {
        "id": nuevo_curso.id,
        "title": nuevo_curso.title,
        "canonical_url": nuevo_curso.canonical_url,
        "platform": nuevo_curso.platform,
        "technology": nuevo_curso.technology,
        "level": nuevo_curso.level,
        "status": nuevo_curso.status
    }

@app.post("/aportes/{course_id}/moderar")
@app.post("/api/aportes/{course_id}/moderar")
def moderar_aporte(
    course_id: str,
    payload: ModerarPayloadSchema,
    x_user_role: Optional[str] = Header(None, alias="X-User-Role"),
    db: Session = Depends(get_db)
):
    # Validar permisos: validador sin rol -> 403
    try:
        validar_permisos_moderacion(x_user_role)
    except AportePermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    repo = CursoRepository(db)
    curso = repo.get_by_id(course_id)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado.")

    # Validar transición y reglas de negocio de moderación
    try:
        nuevo_estado = validar_decision_moderacion(
            estado_actual=curso.status,
            decision=payload.decision,
            motivo_rechazo=payload.rejection_reason
        )
    except (AporteStateError, AporteValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    curso_actualizado = repo.update(course_id, {
        "status": nuevo_estado,
        "rejection_reason": payload.rejection_reason if nuevo_estado == "REJECTED" else None
    })

    return {
        "id": curso_actualizado.id,
        "title": curso_actualizado.title,
        "status": curso_actualizado.status,
        "rejection_reason": curso_actualizado.rejection_reason
    }
