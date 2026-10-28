import pytest
from app.cursos.rules import (
    CourseStatus,
    DomainValidationError,
    InvalidStateTransitionError,
    validar_aporte_curso,
    transicionar_estado_curso,
)

# ==============================================================================
# Tests: Validación de aporte de cursos
# ==============================================================================

def test_validar_aporte_curso_datos_completos_retorna_true():
    # Arrange
    aporte_valido = {
        "title": "FastAPI Avanzado y Arquitectura",
        "url": "https://cursolandia.com/fastapi",
        "platform": "YouTube",
        "technology": "Python",
        "level": "Intermedio"
    }

    # Act
    resultado = validar_aporte_curso(aporte_valido)

    # Assert
    assert resultado is True


def test_validar_aporte_curso_titulo_corto_lanza_excepcion():
    # Arrange
    aporte_invalido = {
        "title": "Fast",
        "url": "https://cursolandia.com/fastapi",
        "platform": "YouTube",
        "technology": "Python",
        "level": "Intermedio"
    }

    # Act & Assert
    with pytest.raises(DomainValidationError, match="al menos 5 caracteres"):
        validar_aporte_curso(aporte_invalido)


def test_validar_aporte_curso_url_invalida_lanza_excepcion():
    # Arrange
    aporte_invalido = {
        "title": "Curso Docker Práctico",
        "url": "ftp://servidor-local/curso",
        "platform": "Drive",
        "technology": "DevOps",
        "level": "Principiante"
    }

    # Act & Assert
    with pytest.raises(DomainValidationError, match="URL del curso debe tener un formato válido"):
        validar_aporte_curso(aporte_invalido)


def test_validar_aporte_curso_nivel_no_permitido_lanza_excepcion():
    # Arrange
    aporte_invalido = {
        "title": "Testing con Pytest",
        "url": "https://youtube.com/watch?v=123",
        "platform": "YouTube",
        "technology": "Python",
        "level": "ExpertoLegendario"
    }

    # Act & Assert
    with pytest.raises(DomainValidationError, match="Nivel inválido"):
        validar_aporte_curso(aporte_invalido)


# ==============================================================================
# Tests: Transiciones de estado (Máquina de estados)
# ==============================================================================

def test_transicionar_estado_curso_de_pending_a_published_exitoso():
    # Arrange
    estado_actual = CourseStatus.PENDING
    nuevo_estado = CourseStatus.PUBLISHED

    # Act
    resultado = transicionar_estado_curso(estado_actual, nuevo_estado)

    # Assert
    assert resultado == CourseStatus.PUBLISHED


def test_transicionar_estado_curso_de_pending_a_rejected_exitoso():
    # Arrange
    estado_actual = CourseStatus.PENDING
    nuevo_estado = CourseStatus.REJECTED

    # Act
    resultado = transicionar_estado_curso(estado_actual, nuevo_estado)

    # Assert
    assert resultado == CourseStatus.REJECTED


def test_transicionar_estado_curso_de_rejected_a_published_lanza_excepcion():
    # Arrange
    estado_actual = CourseStatus.REJECTED
    nuevo_estado = CourseStatus.PUBLISHED

    # Act & Assert
    with pytest.raises(InvalidStateTransitionError, match="Transición inválida"):
        transicionar_estado_curso(estado_actual, nuevo_estado)


def test_transicionar_estado_curso_de_published_a_pending_lanza_excepcion():
    # Arrange
    estado_actual = CourseStatus.PUBLISHED
    nuevo_estado = CourseStatus.PENDING

    # Act & Assert
    with pytest.raises(InvalidStateTransitionError, match="Transición inválida"):
        transicionar_estado_curso(estado_actual, nuevo_estado)
