from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.basemodel import BaseModel


class DatasetModel(BaseModel):
    __tablename__ = 'dataset'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str] = mapped_column('name', String(256))
    path: Mapped[str] = mapped_column('path', String(1024))
    fileSets: Mapped[List['FileSetModel']] = relationship(back_populates='dataset', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'DatasetModel(id={self.id}, path={self.path}, name={self.name})'
