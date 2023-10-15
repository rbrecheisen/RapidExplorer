from sqlalchemy.orm import Session

from rapidx.app.dataset import Dataset
from rapidx.app.fileset import FileSet
from rapidx.app.file import File
from rapidx.app.datasetmodel import DatasetModel
from rapidx.app.filesetmodel import FileSetModel
from rapidx.app.filemodel import FileModel
from rapidx.app.db import DbSession


class DatasetStorageManager:
    def save(self, dataset: Dataset):
        with DbSession() as session:
            datasetModel = DatasetModel(path=dataset.path(), name=dataset.name())
            for fileSet in dataset.fileSets():
                fileSetModel = FileSetModel(path=fileSet.path(), name=fileSet.name(), dataset=datasetModel)
                for file in fileSet.files():
                    fileModel = FileModel(path=file.path(), fileSet=fileSetModel)
                    session.add(fileModel)
                session.add(fileSetModel)
            session.add(datasetModel)
            session.commit()
        return dataset.name

    def load(self, name: str):
        with DbSession() as session:
            datasetModel = session.query(DatasetModel).filter_by(name=name).one()
            dataset = Dataset(path=datasetModel.path, name=datasetModel.name)
            for fileSetModel in datasetModel.fileSets:
                fileSet = FileSet(path=fileSetModel.path, name=fileSetModel.name)
                for fileModel in fileSetModel.files:
                    file = File(path=fileModel.path)
                    fileSet.files.append(file)
                dataset.fileSets.append(fileSet)
        return dataset

    def delete(self, name: str):
        with DbSession() as session:
            datasetModel = session.query(DatasetModel).filter_by(name=name).one()
            session.delete(datasetModel)