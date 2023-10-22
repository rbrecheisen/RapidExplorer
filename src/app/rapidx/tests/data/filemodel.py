from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rapidx.tests.data.basemodel import BaseModel


class FileModel(BaseModel):
    __tablename__ = '_filemodel'
    _id: Mapped[int] = mapped_column('_id', primary_key=True)
    _path: Mapped[str] = mapped_column('_path', String(1024))
    _fileSetModel: Mapped['FileSetModel'] = relationship(back_populates='_fileModels')
    _fileSetModelId: Mapped[int] = mapped_column('_filesetmodel_id', ForeignKey('_filesetmodel._id'))

    def id(self):
        return self._id
    
    def path(self):
        return self._path
    
    def fileSetModel(self):
        return self._fileSetModel
    
    def __str__(self):
        return f'FileModel(id={self.id()}, path={self.path()}, fileSet={self.fileSetModel.id()})'
