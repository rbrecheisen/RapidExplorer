from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rapidx.app.basemodel import BaseModel


class FileModel(BaseModel):
    __tablename__ = 'file'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    path: Mapped[str] = mapped_column('path', String(1024))
    fileSet: Mapped['FileSetModel'] = relationship(back_populates='files')
    fileSetId: Mapped[int] = mapped_column('fileset_id', ForeignKey('fileset.id'))

    def __str__(self) -> str:
        return f'FileModel(id={self.id}, path={self.path})'