from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import create_engine

from datasetloader import DatasetLoader


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
    loader = DatasetLoader(path='/Users/ralph/Desktop/downloads/dataset')
    dataset = loader.execute()

    # Create dataset storage manager?
    datasetObj = Dataset(path=dataset.path)
    for fileSet in dataset.fileSets:
        fileSetObj = FileSet(path=fileSet.path, dataset=datasetObj)
        for file in fileSet.files:            
            fileObj = File(path=file.path, fileSet=fileSetObj)
            session.add(fileObj)
        session.add(fileSetObj)
    session.add(datasetObj)
    session.commit()
