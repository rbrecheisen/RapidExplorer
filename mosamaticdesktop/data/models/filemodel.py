import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from mosamaticdesktop.data.models.basemodel import BaseModel


class FileModel(BaseModel):
    __tablename__ = '_filemodel'
    id: Mapped[str] = Column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name: Mapped[str] = Column('_name', String(256), nullable=False)
    path: Mapped[str] = Column('_path', String(1024), nullable=False)
    fileSetModel: Mapped['FileSetModel'] = relationship('FileSetModel', back_populates='fileModels')
    fileSetModelId: Mapped[str] = Column('_filesetmodel_id', ForeignKey('_filesetmodel._id'))
