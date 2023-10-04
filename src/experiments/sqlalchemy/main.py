import enum

from abc import ABC
from typing import List
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class Dataset(Base):
    __tablename__ = 'dataset'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    path: Mapped[str] = mapped_column('path', String(1024))
    fileSets: Mapped[List['FileSet']] = relationship(back_populates='dataset', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'Dataset(id={self.id}, path={self.path})'
    

class FileSet(Base):
    __tablename__ = 'fileset'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    path: Mapped[str] = mapped_column('path', String(1024))
    dataset: Mapped['Dataset'] = relationship(back_populates='fileSets')
    datasetId: Mapped[int] = mapped_column('dataset_id', ForeignKey('dataset.id'))
    files: Mapped[List['File']] = relationship(back_populates='fileSet', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'FileSet(id={self.id}, path={self.path}, dataset={self.dataset})'
    

class File(Base):
    __tablename__ = 'file'
    id: Mapped[int] = mapped_column('id', primary_key=True)
    path: Mapped[str] = mapped_column('path', String(1024))
    fileSet: Mapped['FileSet'] = relationship(back_populates='files')
    fileSetId: Mapped[int] = mapped_column('fileset_id', ForeignKey('fileset.id'))

    def __repr__(self) -> str:
        return f'File(id={self.id}, path={self.path}, fileSet={self.fileSet})'
    

# Run experiments
engine = create_engine('sqlite://', echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    dataset = Dataset(path='/path/to/dataset')
    fileSet = FileSet(path='/path/to/dataset/fileSet', dataset=dataset)
    file = File(path='/path/to/dataset/fileSet/file', fileSet=fileSet)
    session.add_all([dataset, fileSet, file])
    session.commit()
