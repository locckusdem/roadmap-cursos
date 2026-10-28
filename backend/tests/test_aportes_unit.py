import pytest
from app.aportes.rules import (
    AportePermissionError,
    AporteStateError,
    AporteValidationError,
    validar_permisos_moderacion,
    validar_decision_moderacion,
)

# ==============================================================================
# Tests: Permisos del validador / moderador
# ==============================================================================

def test_validar_permisos_moderacion_rol_moderator_retorna_true():
    # Arrange
    rol_validador = "MODERATOR"

    # Act
    resultado = validar_permisos_moderacion(rol_validador)

    # Assert
    assert resultado is True


def test_validar_permisos_moderacion_rol_user_lanza_permiso_error():
    # Arrange
    rol_estudiante = "USER"

    # Act & Assert
    with pytest.raises(AportePermissionError) as exc_info:
        validar_permisos_moderacion(rol_estudiante)
    assert exc_info.value.code == "FORBIDDEN_MODERATOR_REQUIRED"


def test_validar_permisos_moderacion_sin_rol_lanza_permiso_error():
    # Arrange
    rol_vacio = None

    # Act & Assert
    with pytest.raises(AportePermissionError) as exc_info:
        validar_permisos_moderacion(rol_vacio)
    assert exc_info.value.code == "FORBIDDEN_MODERATOR_REQUIRED"


# ==============================================================================
# Tests: Transición de estado en moderación
# ==============================================================================

def test_validar_decision_moderacion_aprobar_pending_retorna_published():
    # Arrange
    estado_actual = "PENDING"
    decision = "APPROVED"

    # Act
    nuevo_estado = validar_decision_moderacion(estado_actual, decision)

    # Assert
    assert nuevo_estado == "PUBLISHED"


def test_validar_decision_moderacion_rechazar_pending_con_motivo_retorna_rejected():
    # Arrange
    estado_actual = "PENDING"
    decision = "REJECTED"
    motivo = "El enlace no corresponde a un curso completo."

    # Act
    nuevo_estado = validar_decision_moderacion(estado_actual, decision, motivo_rechazo=motivo)

    # Assert
    assert nuevo_estado == "REJECTED"


def test_validar_decision_moderacion_rechazar_sin_motivo_lanza_validation_error():
    # Arrange
    estado_actual = "PENDING"
    decision = "REJECTED"
    motivo_invalido = ""

    # Act & Assert
    with pytest.raises(AporteValidationError) as exc_info:
        validar_decision_moderacion(estado_actual, decision, motivo_rechazo=motivo_invalido)
    assert exc_info.value.code == "REJECTION_REASON_REQUIRED"


def test_validar_decision_moderacion_rechazar_motivo_corto_lanza_validation_error():
    # Arrange
    estado_actual = "PENDING"
    decision = "REJECTED"
    motivo_corto = "mal"

    # Act & Assert
    with pytest.raises(AporteValidationError) as exc_info:
        validar_decision_moderacion(estado_actual, decision, motivo_rechazo=motivo_corto)
    assert exc_info.value.code == "REJECTION_REASON_REQUIRED"


def test_validar_decision_moderacion_curso_ya_publicado_lanza_state_error():
    # Arrange
    estado_actual = "PUBLISHED"
    decision = "APPROVED"

    # Act & Assert
    with pytest.raises(AporteStateError) as exc_info:
        validar_decision_moderacion(estado_actual, decision)
    assert exc_info.value.code == "COURSE_NOT_IN_PENDING_STATE"


def test_validar_decision_moderacion_curso_ya_rechazado_lanza_state_error():
    # Arrange
    estado_actual = "REJECTED"
    decision = "APPROVED"

    # Act & Assert
    with pytest.raises(AporteStateError) as exc_info:
        validar_decision_moderacion(estado_actual, decision)
    assert exc_info.value.code == "COURSE_NOT_IN_PENDING_STATE"


def test_validar_decision_moderacion_decision_invalida_lanza_state_error():
    # Arrange
    estado_actual = "PENDING"
    decision_invalida = "ARCHIVAR"

    # Act & Assert
    with pytest.raises(AporteStateError) as exc_info:
        validar_decision_moderacion(estado_actual, decision_invalida)
    assert exc_info.value.code == "UNKNOWN_MODERATION_DECISION"
