import uuid

from typing import List
from sqlalchemy import String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rapidx.app.utils import create_random_name
from rapidx.app.data.basemodel import BaseModel



class MultiFileSetModel(BaseModel):
    __tablename__ = '_multifilesetmodel'
    id: Mapped[str] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    unboundId: Mapped[str] = mapped_column('_unboundId', String, unique=True, nullable=True)
    name: Mapped[str] = mapped_column('_name', String(256), nullable=True)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    fileSetModels: Mapped[List['FileSetModel']] = relationship(back_populates='multiFileSetModel', cascade='all, delete-orphan')

    def __init__(self, name=None, path=None):
        super(MultiFileSetModel, self).__init__()
        self.name = name
        if not self.name:
            self.name = create_random_name(prefix='multifileset')
        self.path = path

    def firstFileSetModel(self):
        if len(self.fileSetModels) > 0:
            return self.fileSetModels[0]
        return None

    def __str__(self):
        s  = f'MultiFileSetModel(id={self.id}, '
        s += f'name={self.name}, '
        s += f'path={self.path}, '
        s += f'fileSetModels={len(self.fileSetModels)}'
        return s


@event.listens_for(MultiFileSetModel, 'after_insert')
def afterInsert(_, connection, target):
    target.unboundId = target.id
    connection.execute(
        MultiFileSetModel.__table__.update().where(MultiFileSetModel.id == target.id).values(unboundId=target.unboundId))