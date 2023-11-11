import uuid

from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.basemodel import BaseModel


class MultiFileSetModel(BaseModel):
    __tablename__ = '_multifilesetmodel'
    id: Mapped[str] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name: Mapped[str] = mapped_column('_name', String(256), nullable=True)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    fileSetModels: Mapped[List['FileSetModel']] = relationship(back_populates='multiFileSetModel', cascade='all, delete-orphan')
