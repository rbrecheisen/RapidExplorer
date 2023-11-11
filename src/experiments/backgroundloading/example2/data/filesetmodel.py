import uuid

from typing import List
from sqlalchemy import String, ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.basemodel import BaseModel
from utils import create_random_name


class FileSetModel(BaseModel):
    __tablename__ = '_filesetmodel'
    id: Mapped[int] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name: Mapped[str] = mapped_column('_name', String(256), nullable=True)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    multiFileSetModel: Mapped['MultiFileSetModel'] = relationship(back_populates='fileSetModels')
    multiFileSetModelId: Mapped[int] = mapped_column('_multifilesetmodel_id', ForeignKey('_multifilesetmodel._id'))
    fileModels: Mapped[List['FileModel']] = relationship(back_populates='fileSetModel', cascade='all, delete-orphan')


@event.listens_for(FileSetModel, 'after_insert')
def afterInsert(_, connection, target):
    if not target.name:
        target.name = create_random_name(prefix='fileset')
        connection.execute(
            FileSetModel.__table__.update().where(FileSetModel.id == target.id).values(name=target.name))