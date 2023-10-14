from sqlalchemy.orm import Session

from dataset import Dataset
from fileset import FileSet
from file import File
from datasetmodel import DatasetModel
from filesetmodel import FileSetModel
from filemodel import FileModel
from db import DbSession


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