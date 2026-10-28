import pytest
from app.roadmaps.rules import (
    RoadmapDomainError,
    validar_agregar_curso_a_roadmap,
    quitar_curso_de_roadmap,
    reordenar_items_roadmap,
)

# ==============================================================================
# Tests: Agregar curso al roadmap
# ==============================================================================

def test_validar_agregar_curso_a_roadmap_curso_publicado_exitoso():
    # Arrange
    roadmap = {"id": "rm-1", "items": []}
    curso_publicado = {
        "id": "c-101",
        "title": "Arquitectura de Software",
        "status": "PUBLISHED"
    }

    # Act
    item_creado = validar_agregar_curso_a_roadmap(roadmap, curso_publicado)

    # Assert
    assert item_creado["course_id"] == "c-101"
    assert item_creado["position"] == 1


def test_validar_agregar_curso_a_roadmap_curso_inexistente_lanza_excepcion():
    # Arrange
    roadmap = {"id": "rm-1", "items": []}
    curso_inexistente = None

    # Act & Assert
    with pytest.raises(RoadmapDomainError, match="El curso no existe"):
        validar_agregar_curso_a_roadmap(roadmap, curso_inexistente)


def test_validar_agregar_curso_a_roadmap_curso_no_publicado_lanza_excepcion():
    # Arrange
    roadmap = {"id": "rm-1", "items": []}
    curso_pendiente = {
        "id": "c-102",
        "title": "FastAPI Testing",
        "status": "PENDING"
    }

    # Act & Assert
    with pytest.raises(RoadmapDomainError, match="Solo se pueden agregar cursos con estado PUBLISHED"):
        validar_agregar_curso_a_roadmap(roadmap, curso_pendiente)


def test_validar_agregar_curso_a_roadmap_curso_duplicado_lanza_excepcion():
    # Arrange
    roadmap = {
        "id": "rm-1",
        "items": [{"course_id": "c-101", "position": 1}]
    }
    curso_duplicado = {
        "id": "c-101",
        "title": "Arquitectura de Software",
        "status": "PUBLISHED"
    }

    # Act & Assert
    with pytest.raises(RoadmapDomainError, match="El curso ya está en el roadmap"):
        validar_agregar_curso_a_roadmap(roadmap, curso_duplicado)


def test_validar_agregar_curso_a_roadmap_limite_alcanzado_lanza_excepcion():
    # Arrange
    limite = 2
    roadmap = {
        "id": "rm-1",
        "items": [
            {"course_id": "c-1", "position": 1},
            {"course_id": "c-2", "position": 2}
        ]
    }
    nuevo_curso = {
        "id": "c-3",
        "title": "Docker Avanzado",
        "status": "PUBLISHED"
    }

    # Act & Assert
    with pytest.raises(RoadmapDomainError, match="límite máximo"):
        validar_agregar_curso_a_roadmap(roadmap, nuevo_curso, max_items=limite)


# ==============================================================================
# Tests: Quitar curso del roadmap
# ==============================================================================

def test_quitar_curso_de_roadmap_existente_reordena_posiciones():
    # Arrange
    roadmap = {
        "id": "rm-1",
        "items": [
            {"course_id": "c-1", "position": 1},
            {"course_id": "c-2", "position": 2},
            {"course_id": "c-3", "position": 3}
        ]
    }

    # Act
    items_actualizados = quitar_curso_de_roadmap(roadmap, course_id="c-2")

    # Assert
    assert len(items_actualizados) == 2
    assert items_actualizados[0]["course_id"] == "c-1"
    assert items_actualizados[0]["position"] == 1
    assert items_actualizados[1]["course_id"] == "c-3"
    assert items_actualizados[1]["position"] == 2


def test_quitar_curso_de_roadmap_inexistente_lanza_excepcion():
    # Arrange
    roadmap = {
        "id": "rm-1",
        "items": [{"course_id": "c-1", "position": 1}]
    }

    # Act & Assert
    with pytest.raises(RoadmapDomainError, match="El curso no pertenece al roadmap"):
        quitar_curso_de_roadmap(roadmap, course_id="c-999")


# ==============================================================================
# Tests: Reordenar items del roadmap
# ==============================================================================

def test_reordenar_items_roadmap_posicion_valida_actualiza_orden():
    # Arrange
    roadmap = {
        "id": "rm-1",
        "items": [
            {"course_id": "c-1", "position": 1},
            {"course_id": "c-2", "position": 2},
            {"course_id": "c-3", "position": 3}
        ]
    }

    # Act: mover c-3 a la primera posición
    items_reordenados = reordenar_items_roadmap(roadmap, course_id="c-3", nueva_posicion=1)

    # Assert
    assert items_reordenados[0]["course_id"] == "c-3"
    assert items_reordenados[0]["position"] == 1
    assert items_reordenados[1]["course_id"] == "c-1"
    assert items_reordenados[1]["position"] == 2
    assert items_reordenados[2]["course_id"] == "c-2"
    assert items_reordenados[2]["position"] == 3


def test_reordenar_items_roadmap_posicion_invalida_lanza_excepcion():
    # Arrange
    roadmap = {
        "id": "rm-1",
        "items": [
            {"course_id": "c-1", "position": 1},
            {"course_id": "c-2", "position": 2}
        ]
    }

    # Act & Assert (intentar mover a posición 0 o mayor a 2)
    with pytest.raises(RoadmapDomainError, match="fuera de rango"):
        reordenar_items_roadmap(roadmap, course_id="c-1", nueva_posicion=0)

    with pytest.raises(RoadmapDomainError, match="fuera de rango"):
        reordenar_items_roadmap(roadmap, course_id="c-1", nueva_posicion=5)


def test_reordenar_items_roadmap_curso_no_presente_lanza_excepcion():
    # Arrange
    roadmap = {
        "id": "rm-1",
        "items": [{"course_id": "c-1", "position": 1}]
    }

    # Act & Assert
    with pytest.raises(RoadmapDomainError, match="El curso no pertenece al roadmap"):
        reordenar_items_roadmap(roadmap, course_id="c-no-existe", nueva_posicion=1)
