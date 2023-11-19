import uuid

from sqlalchemy import String, ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rapidx.app.data.basemodel import BaseModel


class FileModel(BaseModel):
    __tablename__ = '_filemodel'
    id: Mapped[str] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    unboundId: Mapped[str] = mapped_column('_unboundId', String, unique=True, nullable=True)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=False)
    fileSetModel: Mapped['FileSetModel'] = relationship(back_populates='fileModels')
    fileSetModelId: Mapped[int] = mapped_column('_filesetmodel_id', ForeignKey('_filesetmodel._id'))

    def __init__(self, fileSetModel, path):
        self.fileSetModel = fileSetModel
        self.path = path
    
    def __str__(self):
        return f'FileModel(id={self.id}, path={self.path}, fileSet={self.fileSetModel.id})'


@event.listens_for(FileModel, 'after_insert')
def afterInsert(_, connection, target):
    target.unboundId = target.id
    connection.execute(
        FileModel.__table__.update().where(FileModel.id == target.id).values(unboundId=target.unboundId))