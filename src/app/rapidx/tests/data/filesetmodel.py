from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rapidx.tests.data.basemodel import BaseModel
from rapidx.tests.data.filemodel import FileModel
from rapidx.tests.data.multifilesetmodel import MultiFileSetModel


class FileSetModel(BaseModel):
    __tablename__ = '_filesetmodel'
    _id: Mapped[int] = mapped_column('_id', primary_key=True)
    _name: Mapped[str] = mapped_column('_name', String(256), unique=False)
    _path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    _multiFileSetModel: Mapped['MultiFileSetModel'] = relationship(back_populates='_fileSetModels')
    _multiFileSetModelId: Mapped[int] = mapped_column('_multifilesetmodel_id', ForeignKey('_multifilesetmodel._id'))
    _fileModels: Mapped[List['FileModel']] = relationship(back_populates='_fileSetModel', cascade='all, delete-orphan')

    def id(self):
        return self._id
    
    def name(self):
        return self._name
    
    def setName(self, name: str):
        self._name = name
    
    def path(self):
        return self._path
    
    def multiFileSetModel(self):
        return self._multiFileSetModel
    
    def fileModels(self):
        return self._fileModels

    def __str__(self):
        s =  f'FileSetModel(id={self.id()}, '
        s += f'name={self.name()}, '
        s += f'path={self.path()}, ' 
        s += f'multiFileSetModel={self.multiFileSetModel().id()}, '
        s += f'fileModels={len(self.fileModels())}'
        return s
