from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false

from utils.db.base import ModelBase

ModelType = TypeVar("ModelType", bound=ModelBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @staticmethod
    def calc_offset(page: int, per_page: int) -> int:
        return (page - 1) * per_page

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.id == id, self.model.is_deleted == false())
            .first()
        )

    def get_deleted_also(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, page: int = 1, per_page: int = 10
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.is_deleted == false())
            .offset(self.calc_offset(page, per_page))
            .limit(per_page)
            .all()
        )

    def get_multi_deleted_also(
        self, db: Session, *, page: int = 1, per_page: int = 10
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .offset(self.calc_offset(page, per_page))
            .limit(per_page)
            .all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in, exclude_unset=True)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj, exclude_unset=True)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        return db_obj

    def soft_del(self, db: Session, db_obj: ModelType):
        db_obj.is_deleted = True
        db.add(db_obj)
        db.commit()
        return db_obj

    def hard_del(self, db: Session, db_obj: ModelType) -> bool:
        db.delete(db_obj)
        db.commit()
        return True

    def remove_by_id(self, db: Session, *, id: str) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def add_all(
        self, db: Session, *, objs_in: List[CreateSchemaType]
    ) -> List[ModelType]:
        db_objs = [
            self.model(**jsonable_encoder(c, exclude_unset=True)) for c in objs_in
        ]
        db.add_all(db_objs)
        db.commit()
        return db_objs
