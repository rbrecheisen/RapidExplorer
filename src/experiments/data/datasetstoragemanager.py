from sqlalchemy.orm import Session

from dataset import Dataset
from fileset import FileSet
from file import File
from datasetmodel import DatasetModel
from filesetmodel import FileSetModel
from filemodel import FileModel


class DatasetStorageManager:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, dataset: Dataset):
        datasetModel = DatasetModel(path=dataset.path(), name=dataset.name())
        for fileSet in dataset.fileSets():
            fileSetModel = FileSetModel(path=fileSet.path(), name=fileSet.name(), dataset=datasetModel)
            for file in fileSet.files():
                fileModel = FileModel(path=file.path(), fileSet=fileSetModel)
                self._session.add(fileModel)
            self._session.add(fileSetModel)
        self._session.add(datasetModel)
        self._session.commit()
        return dataset.name

    def load(self, name: str):
        datasetModel = self._session.query(DatasetModel).filter_by(name=name).one()
        dataset = Dataset(path=datasetModel.path, name=datasetModel.name)
        for fileSetModel in datasetModel.fileSets:
            fileSet = FileSet(path=fileSetModel.path, name=fileSetModel.name)
            for fileModel in fileSetModel.files:
                file = File(path=fileModel.path)
                fileSet.files.append(file)
            dataset.fileSets.append(fileSet)
        return dataset

    def delete(self, name: str):
        datasetModel = self._session.query(DatasetModel).filter_by(name=name).one()
        self._session.delete(datasetModel)