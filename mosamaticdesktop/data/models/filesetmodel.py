import uuid

from typing import List
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from mosamaticdesktop.data.models.basemodel import BaseModel
from mosamaticdesktop.utils import createNameWithTimestamp


class FileSetModel(BaseModel):
    __tablename__ = '_filesetmodel'
    id: Mapped[int] = Column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name: Mapped[str] = Column('_name', String(256), nullable=False)
    path: Mapped[str] = Column('_path', String(1024), nullable=False)
    fileModels: Mapped[List['FileModel']] = relationship('FileModel', back_populates='fileSetModel', cascade='all, delete-orphan')
