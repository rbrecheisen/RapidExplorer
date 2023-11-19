import uuid

from typing import List
from sqlalchemy import String, ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rapidx.app.utils import create_random_name
from rapidx.app.data.basemodel import BaseModel
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel


class FileSetModel(BaseModel):
    __tablename__ = '_filesetmodel'
    id: Mapped[int] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    unboundId: Mapped[str] = mapped_column('_unboundId', String, unique=True, nullable=True)
    name: Mapped[str] = mapped_column('_name', String(256), nullable=True)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    multiFileSetModel: Mapped['MultiFileSetModel'] = relationship(back_populates='fileSetModels')
    multiFileSetModelId: Mapped[int] = mapped_column('_multifilesetmodel_id', ForeignKey('_multifilesetmodel._id'))
    fileModels: Mapped[List['FileModel']] = relationship(back_populates='fileSetModel', cascade='all, delete-orphan')

    def __init__(self, multiFileSetModel, name=None, path=None):
        super(FileSetModel, self).__init__()
        self.multiFileSetModel = multiFileSetModel
        self.name = name
        if not self.name:
            self.name = create_random_name(prefix='fileset')
        self.path = path

    def firstFileModel(self):
        if len(self.fileModels) > 0:
            return self.fileModels[0]
        return None

    def __str__(self):
        s =  f'FileSetModel(id={self.id}, '
        s += f'name={self.name}, '
        s += f'path={self.path}, ' 
        s += f'multiFileSetModel={self.multiFileSetModel().id}, '
        s += f'fileModels={len(self.fileModels)}'
        return s


@event.listens_for(FileSetModel, 'after_insert')
def afterInsert(_, connection, target):
    target.unboundId = target.id
    connection.execute(
        FileSetModel.__table__.update().where(FileSetModel.id == target.id).values(unboundId=target.unboundId))