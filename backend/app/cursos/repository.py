from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.cursos.models import Course

class CursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: Dict[str, Any]) -> Course:
        curso = Course(**data)
        self.db.add(curso)
        self.db.commit()
        self.db.refresh(curso)
        return curso

    def get_by_id(self, course_id: str) -> Optional[Course]:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def list_paginated(
        self,
        page: int = 1,
        size: int = 20,
        q: Optional[str] = None,
        category_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Course], int]:
        query = self.db.query(Course)

        if status:
            query = query.filter(Course.status == status)

        if category_id is not None:
            query = query.filter(Course.category_id == category_id)

        if q:
            filtro_q = f"%{q.strip().lower()}%"
            query = query.filter(
                func.lower(Course.title).like(filtro_q) |
                func.lower(Course.technology).like(filtro_q)
            )

        total_count = query.count()
        offset = max(0, (page - 1) * size)
        items = query.order_by(Course.created_at.desc()).offset(offset).limit(size).all()

        return items, total_count

    def update(self, course_id: str, fields: Dict[str, Any]) -> Optional[Course]:
        curso = self.get_by_id(course_id)
        if not curso:
            return None

        for key, value in fields.items():
            if hasattr(curso, key):
                setattr(curso, key, value)

        self.db.commit()
        self.db.refresh(curso)
        return curso

    def delete(self, course_id: str) -> bool:
        curso = self.get_by_id(course_id)
        if not curso:
            return False

        self.db.delete(curso)
        self.db.commit()
        return True
