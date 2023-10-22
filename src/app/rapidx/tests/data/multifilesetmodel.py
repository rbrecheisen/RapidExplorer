from typing import List
from sqlalchemy import create_engine, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rapidx.tests.data.basemodel import BaseModel



class MultiFileSetModel(BaseModel):
    __tablename__ = '_multifilesetmodel'
    _id: Mapped[int] = mapped_column('_id', primary_key=True)
    _name: Mapped[str] = mapped_column('_name', String(256))
    _path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    _fileSetModels: Mapped[List['FileSetModel']] = relationship(back_populates='_multiFileSetModel', cascade='all, delete-orphan')

    def id(self):
        return self._id
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def fileSetModels(self):
        return self._fileSetModels

    def __str__(self):
        s  = f'MultiFileSetModel(id={self.id()}, '
        s += f'name={self.name()}, '
        s += f'path={self.path()}, '
        s += f'fileSetModels={len(self.fileSetModels())}'
        return s
