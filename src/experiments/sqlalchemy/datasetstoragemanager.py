from sqlalchemy.orm import Session

from models.dataset import Dataset
from models.fileset import FileSet
from models.file import File
from models.datasetmodel import DatasetModel
from models.filesetmodel import FileSetModel
from models.filemodel import FileModel


class DatasetStorageManager:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, dataset: Dataset):
        datasetModel = DatasetModel(path=dataset.path, name=dataset.name)
        for fileSet in dataset.fileSets:
            fileSetModel = FileSetModel(path=fileSet.path, dataset=datasetModel)
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
            fileSet = FileSet(path=fileSetModel.path)
            for fileModel in fileSetModel.files:
                file = File(path=fileModel.path)
                fileSet.files.append(file)
            dataset.fileSets.append(fileSet)
        return dataset

    def delete(self, name: str):
        datasetModel = self.session.query(DatasetModel).filter_by(name=name).one()
        self.session.delete(datasetModel)