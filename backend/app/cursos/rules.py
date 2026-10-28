from enum import Enum
import re
from datetime import datetime
from typing import Dict, Any, Optional, Set

class CourseStatus(str, Enum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"

VALID_LEVELS = {"Principiante", "Intermedio", "Avanzado"}
URL_REGEX = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)

class DomainValidationError(Exception):
    """Excepción de negocio ante datos de curso inválidos."""
    pass

class InvalidStateTransitionError(Exception):
    """Excepción cuando una transición de estado no está permitida."""
    pass

def validar_aporte_curso(data: Dict[str, Any], existing_urls: Optional[Set[str]] = None) -> bool:
    """
    Función pura para validar la postulación de un curso.
    Lanza DomainValidationError si no cumple las reglas de negocio.
    """
    titulo = data.get("title", "").strip()
    if not titulo or len(titulo) < 5:
        raise DomainValidationError("El título debe tener al menos 5 caracteres.")
    
    url = data.get("url", "").strip()
    if not url or not URL_REGEX.match(url):
        raise DomainValidationError("La URL del curso debe tener un formato válido (http/https).")
    
    if existing_urls is not None and url in existing_urls:
        raise DomainValidationError("La URL del curso ya ha sido postulada anteriormente.")

    platform = data.get("platform", "").strip()
    if not platform:
        raise DomainValidationError("La plataforma proveedora es obligatoria.")
    
    technology = data.get("technology", "").strip()
    if not technology:
        raise DomainValidationError("La tecnología del curso es obligatoria.")
        
    level = data.get("level", "").strip()
    if level not in VALID_LEVELS:
        raise DomainValidationError(f"Nivel inválido. Debe ser uno de: {', '.join(VALID_LEVELS)}.")

    edition_year = data.get("edition_year")
    if edition_year is not None:
        current_year = datetime.now().year
        if not isinstance(edition_year, int) or edition_year > current_year + 1 or edition_year < 1990:
            raise DomainValidationError("El año de edición no puede ser en el futuro ni anterior a 1990.")

    for flag in ["has_quizzes", "requires_exam", "grants_certificate"]:
        if flag in data and not isinstance(data[flag], bool):
            raise DomainValidationError(f"El campo {flag} debe ser un valor booleano.")

    return True

def transicionar_estado_curso(estado_actual: CourseStatus, nuevo_estado: CourseStatus) -> CourseStatus:
    """
    Función pura que controla la máquina de estados de un curso.
    Solo un curso PENDING puede ser aprobado (PUBLISHED) o rechazado (REJECTED).
    """
    transiciones_validas = {
        CourseStatus.PENDING: {CourseStatus.PUBLISHED, CourseStatus.REJECTED},
        CourseStatus.PUBLISHED: set(),  # Estado terminal para el flujo básico
        CourseStatus.REJECTED: set(),   # Estado terminal
    }

    if nuevo_estado not in transiciones_validas.get(estado_actual, set()):
        raise InvalidStateTransitionError(
            f"Transición inválida: no se puede pasar de {estado_actual.value} a {nuevo_estado.value}."
        )

    return nuevo_estado
