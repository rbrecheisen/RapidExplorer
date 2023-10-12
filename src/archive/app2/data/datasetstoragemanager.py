from sqlalchemy.orm import Session

from data.models.dataset import Dataset
from data.models.fileset import FileSet
from data.models.file import File
from data.models.datasetmodel import DatasetModel
from data.models.filesetmodel import FileSetModel
from data.models.filemodel import FileModel


class DatasetStorageManager:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, dataset: Dataset):
        datasetModel = DatasetModel(path=dataset.path, name=dataset.name)
        for fileSet in dataset.fileSets:
            fileSetModel = FileSetModel(path=fileSet.path, name=fileSet.name, dataset=datasetModel)
            for file in fileSet.files:
                fileModel = FileModel(path=file.path, fileSet=fileSetModel)
                self.session.add(fileModel)
            self.session.add(fileSetModel)
        self.session.add(datasetModel)
        self.session.commit()
        return dataset.name

    def load(self, name: str):
        datasetModel = self.session.query(DatasetModel).filter_by(name=name).one()
        # convert back to dataset
        dataset = Dataset(path=datasetModel.path, name=datasetModel.name)
        for fileSetModel in datasetModel.fileSets:
            fileSet = FileSet(path=fileSetModel.path, name=fileSetModel.name)
            for fileModel in fileSetModel.files:
                file = File(path=fileModel.path)
                fileSet.files.append(file)
            dataset.fileSets.append(fileSet)
        return dataset

    def delete(self, name: str):
        datasetModel = self.session.query(DatasetModel).filter_by(name=name).one()
        self.session.delete(datasetModel)