import uuid

from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rapidx.app.data.basemodel import BaseModel



class MultiFileSetModel(BaseModel):
    __tablename__ = '_multifilesetmodel'
    _id: Mapped[int] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    _name: Mapped[str] = mapped_column('_name', String(256), nullable=True)
    _path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    _fileSetModels: Mapped[List['FileSetModel']] = relationship(back_populates='_multiFileSetModel', cascade='all, delete-orphan')

    def id(self):
        return self._id
    
    def name(self):
        return self._name
    
    def setName(self, name: str):
        self._name = name
    
    def path(self):
        return self._path
    
    def fileSetModels(self):
        return self._fileSetModels
    
    def nrFileSetModels(self):
        return len(self.fileSetModels())
    
    def firstFileSetModel(self):
        if self.nrFileSetModels() > 0:
            return self.fileSetModels() [0]
        return None

    def __str__(self):
        s  = f'MultiFileSetModel(id={self.id()}, '
        s += f'name={self.name()}, '
        s += f'path={self.path()}, '
        s += f'fileSetModels={len(self.fileSetModels())}'
        return s
