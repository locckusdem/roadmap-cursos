from typing import Optional

class AporteModeracionError(Exception):
    """Excepción base con código de error semántico y estable."""
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code
        self.message = message

class AportePermissionError(AporteModeracionError):
    def __init__(self, message: str = "Permiso denegado: se requiere rol MODERATOR."):
        super().__init__(message, code="FORBIDDEN_MODERATOR_REQUIRED")

class AporteStateError(AporteModeracionError):
    def __init__(self, message: str = "Estado inválido para la operación de moderación.", code: str = "INVALID_MODERATION_STATE"):
        super().__init__(message, code=code)

class AporteValidationError(AporteModeracionError):
    def __init__(self, message: str = "Validación fallida en los datos de moderación.", code: str = "VALIDATION_FAILED"):
        super().__init__(message, code=code)

def validar_permisos_moderacion(user_role: Optional[str]) -> bool:
    """
    Función pura que valida si el usuario cuenta con rol MODERATOR.
    Lanza AportePermissionError si el rol no es adecuado.
    """
    if not user_role or user_role.upper() != "MODERATOR":
        raise AportePermissionError("Solo los usuarios con rol MODERATOR pueden moderar aportes.")
    return True

def validar_decision_moderacion(
    estado_actual: str,
    decision: str,
    motivo_rechazo: Optional[str] = None
) -> str:
    """
    Función pura para validar la acción de moderar un curso.
    Solo admite evaluar cursos PENDING hacia PUBLISHED o REJECTED.
    Para rechazar, exige un motivo_rechazo válido de al menos 5 caracteres.
    Retorna el nuevo estado ('PUBLISHED' o 'REJECTED').
    """
    if estado_actual != "PENDING":
        raise AporteStateError(
            f"No se puede moderar un curso con estado '{estado_actual}'. Solo se admiten cursos PENDING.",
            code="COURSE_NOT_IN_PENDING_STATE"
        )

    decision_normalizada = decision.upper()
    if decision_normalizada not in {"APPROVED", "REJECTED"}:
        raise AporteStateError(
            f"Decisión '{decision}' desconocida. Debe ser 'APPROVED' o 'REJECTED'.",
            code="UNKNOWN_MODERATION_DECISION"
        )

    if decision_normalizada == "REJECTED":
        if not motivo_rechazo or len(motivo_rechazo.strip()) < 5:
            raise AporteValidationError(
                "El motivo de rechazo es obligatorio y debe tener al menos 5 caracteres.",
                code="REJECTION_REASON_REQUIRED"
            )
        return "REJECTED"

    return "PUBLISHED"
