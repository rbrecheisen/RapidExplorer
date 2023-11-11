import os
import uuid

from typing import List
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

DATABASE = 'db.complex.sqlite3'
ECHO = False
MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


class BaseModel(DeclarativeBase):
    pass

class FileModel(BaseModel):
    __tablename__ = '_filemodel'
    id: Mapped[str] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=False)
    fileSetModel: Mapped['FileSetModel'] = relationship(back_populates='fileModels')
    fileSetModelId: Mapped[int] = mapped_column('_filesetmodel_id', ForeignKey('_filesetmodel._id'))

class FileSetModel(BaseModel):
    __tablename__ = '_filesetmodel'
    id: Mapped[int] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name: Mapped[str] = mapped_column('_name', String(256), nullable=True)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    multiFileSetModel: Mapped['MultiFileSetModel'] = relationship(back_populates='fileSetModels')
    multiFileSetModelId: Mapped[int] = mapped_column('_multifilesetmodel_id', ForeignKey('_multifilesetmodel._id'))
    fileModels: Mapped[List['FileModel']] = relationship(back_populates='fileSetModel', cascade='all, delete-orphan')

class MultiFileSetModel(BaseModel):
    __tablename__ = '_multifilesetmodel'
    id: Mapped[str] = mapped_column('_id', String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name: Mapped[str] = mapped_column('_name', String(256), nullable=True)
    path: Mapped[str] = mapped_column('_path', String(1024), nullable=True)
    fileSetModels: Mapped[List['FileSetModel']] = relationship(back_populates='multiFileSetModel', cascade='all, delete-orphan')
    pass

class LoadedMultiFileSetModel:
    def __init__(self, multiFileSetModel: MultiFileSetModel):
        self.id = multiFileSetModel.id
        self.name = multiFileSetModel.name
        self.path = multiFileSetModel.path
        self.loadedFileSetModels = []

class LoadedFileSetModel:
    def __init__(self, fileSetModel: FileSetModel, LoadedMultiFileSetModel: LoadedMultiFileSetModel):
        self.id = fileSetModel.id
        self.name = fileSetModel.name
        self.path = fileSetModel.path
        self.loadMultiFileSetModel = LoadedMultiFileSetModel
        self.loadedFileModels = []

class LoadedFileModel:
    def __init__(self, fileModel: FileModel, loadedFileSetModel: LoadedFileSetModel):
        self.id = fileModel.id
        self.path = fileModel.path
        self.loadFileSetModel = loadedFileSetModel

class Db:
    def __init__(self) -> None:
        super(Db, self).__init__()
        self._engine = create_engine(f'sqlite:///{DATABASE}', echo=ECHO)
        BaseModel.metadata.create_all(self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def session(self):
        return self._session

class FileRegistrar:    
    def execute(self, filePath):
        pass

class FileImporter:
    def execute(self):
        registrar = FileRegistrar()
        multiFileSetModel = registrar.execute(FILEPATH)
        print(multiFileSetModel.id)

class FileLoader:
    pass

def printLoadedMultiFileSetModel(loadedMultiFileSetModel: LoadedMultiFileSetModel):
    print(f'loadedMultiFileSetModel.id = {loadedMultiFileSetModel.id}')
    for loadedFileSetModel in loadedMultiFileSetModel.loadedFileSetModels:
        print(f'loadedFileSetModel.id = {loadedFileSetModel.id}')
        for loadedFileModel in loadedFileSetModel.loadedFileModels:
            print(f'loadedFileModel.id = {loadedFileModel.id}')

def main():

    session = Db().session()
    multiFileSetModel = MultiFileSetModel()
    session.add(multiFileSetModel)
    session.commit()
    loadedMultiFileSetModel = LoadedMultiFileSetModel(multiFileSetModel)
    fileSetModel = FileSetModel(path=FILESETPATH, multiFileSetModel=multiFileSetModel)
    session.add(fileSetModel)
    session.commit()
    loadedFileSetModel = LoadedFileSetModel(fileSetModel, loadedMultiFileSetModel)
    fileModel = FileModel(path=FILEPATH, fileSetModel=fileSetModel)
    session.add(fileModel)
    session.commit()
    loadedFileModel = LoadedFileModel(fileModel, loadedFileSetModel)
    session.close()

    loadedFileSetModel.loadedFileModels.append(loadedFileModel)
    loadedMultiFileSetModel.loadedFileSetModels.append(loadedFileSetModel)

    printLoadedMultiFileSetModel(loadedMultiFileSetModel)

    # session = Db().session()
    # multiFileSetModel = session.get(MultiFileSetModel, loadedMultiFileSetModel.id)
    # print(multiFileSetModel.id)
    # fileSetModels = session.query(FileSetModel).filter_by(multiFileSetModel=multiFileSetModel).all()
    # for fileSetModel in fileSetModels:
    #     print(fileSetModel.id)
    #     fileModels = session.query(FileModel).filter_by(fileSetModel=fileSetModel).all()
    #     for fileModel in fileModels:
    #         print(fileModel.id)
    # session.close()

if __name__ == '__main__':
    main()
