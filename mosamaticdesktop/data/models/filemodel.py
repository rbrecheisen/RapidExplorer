import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mosamaticdesktop.data.models.basemodel import BaseModel


class FileModel(BaseModel):
    __tablename__ = '_filemodel'
    id: Mapped[str] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name: Mapped[str] = mapped_column('_name', String(256), nullable=False)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=False)
    fileSetModel: Mapped['FileSetModel'] = relationship(back_populates='fileModels')
    fileSetModelId: Mapped[str] = mapped_column('_filesetmodel_id', ForeignKey('_filesetmodel._id'))
