from typing import Dict, Any, List, Optional

class RoadmapDomainError(Exception):
    """Excepción de negocio para operaciones sobre roadmaps."""
    pass

MAX_ROADMAP_ITEMS_DEFAULT = 50

def validar_agregar_curso_a_roadmap(
    roadmap: Dict[str, Any],
    curso: Optional[Dict[str, Any]],
    max_items: int = MAX_ROADMAP_ITEMS_DEFAULT
) -> Dict[str, Any]:
    """
    Función pura para validar y generar la inclusión de un curso en un roadmap.
    Solo admite cursos publicados, previene duplicados y respeta el límite máximo.
    """
    if curso is None:
        raise RoadmapDomainError("El curso no existe.")

    status = curso.get("status")
    if status != "PUBLISHED":
        raise RoadmapDomainError("Solo se pueden agregar cursos con estado PUBLISHED al roadmap.")

    course_id = curso.get("id")
    if not course_id:
        raise RoadmapDomainError("El curso no tiene un identificador válido.")

    items: List[Dict[str, Any]] = roadmap.get("items", [])
    if any(item.get("course_id") == course_id for item in items):
        raise RoadmapDomainError("El curso ya está en el roadmap.")

    if len(items) >= max_items:
        raise RoadmapDomainError(f"Se ha alcanzado el límite máximo de {max_items} cursos en el roadmap.")

    nueva_posicion = len(items) + 1
    return {
        "course_id": course_id,
        "position": nueva_posicion,
        "title": curso.get("title", "")
    }

def quitar_curso_de_roadmap(roadmap: Dict[str, Any], course_id: Any) -> List[Dict[str, Any]]:
    """
    Función pura para quitar un curso del roadmap y recalcular correlativamente las posiciones.
    """
    items: List[Dict[str, Any]] = roadmap.get("items", [])
    indice_encontrado = -1
    for idx, item in enumerate(items):
        if item.get("course_id") == course_id:
            indice_encontrado = idx
            break

    if indice_encontrado == -1:
        raise RoadmapDomainError("El curso no pertenece al roadmap.")

    items_restantes = [item for idx, item in enumerate(items) if idx != indice_encontrado]
    for idx, item in enumerate(items_restantes):
        item["position"] = idx + 1

    return items_restantes

def reordenar_items_roadmap(roadmap: Dict[str, Any], course_id: Any, nueva_posicion: int) -> List[Dict[str, Any]]:
    """
    Función pura para mover un curso a una nueva posición válida (1-indexed)
    y reordenar correlativamente todos los elementos.
    """
    items: List[Dict[str, Any]] = [dict(item) for item in roadmap.get("items", [])]
    total_items = len(items)

    item_a_mover = None
    for item in items:
        if item.get("course_id") == course_id:
            item_a_mover = item
            break

    if item_a_mover is None:
        raise RoadmapDomainError("El curso no pertenece al roadmap.")

    if nueva_posicion < 1 or nueva_posicion > total_items:
        raise RoadmapDomainError("Posición de reordenamiento fuera de rango.")

    items.remove(item_a_mover)
    items.insert(nueva_posicion - 1, item_a_mover)

    for idx, item in enumerate(items):
        item["position"] = idx + 1

    return items
