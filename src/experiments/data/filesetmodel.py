from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from basemodel import BaseModel


class FileSetModel(BaseModel):
    __tablename__ = 'fileset'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str] = mapped_column('name', String(256), unique=False)
    path: Mapped[str] = mapped_column('path', String(1024), nullable=True)
    dataset: Mapped['DatasetModel'] = relationship(back_populates='fileSets')
    datasetId: Mapped[int] = mapped_column('dataset_id', ForeignKey('dataset.id'))
    files: Mapped[List['FileModel']] = relationship(back_populates='fileSet', cascade='all, delete-orphan')