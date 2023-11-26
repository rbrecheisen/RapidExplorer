import uuid

from typing import List
from sqlalchemy import String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.basemodel import BaseModel
from utils import createRandomName


class MultiFileSetModel(BaseModel):
    __tablename__ = '_multifilesetmodel'
    id: Mapped[str] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name: Mapped[str] = mapped_column('_name', String(256), unique=True, nullable=True)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    fileSetModels: Mapped[List['FileSetModel']] = relationship(back_populates='multiFileSetModel', cascade='all, delete-orphan')


@event.listens_for(MultiFileSetModel, 'after_insert')
def afterInsert(_, connection, target):
    if not target.name:
        target.name = createRandomName(prefix='multifileset')
        connection.execute(
            MultiFileSetModel.__table__.update().where(MultiFileSetModel.id == target.id).values(name=target.name))