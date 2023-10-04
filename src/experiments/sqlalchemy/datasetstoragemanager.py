from sqlalchemy.orm import Session

from models.dataset import Dataset
from models.datasetmodel import DatasetModel
from models.filesetmodel import FileSetModel
from models.filemodel import FileModel


class DatasetStorageManager:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, dataset: Dataset):
        print(dataset)
        datasetModel = DatasetModel(path=dataset.path)
        for fileSet in dataset.fileSets:
            fileSetModel = FileSetModel(path=fileSet.path, dataset=datasetModel)
            for file in fileSet.files:
                fileModel = FileModel(path=file.path, fileSet=fileSetModel)
                self.session.add(fileModel)
            self.session.add(fileSetModel)
        self.session.add(datasetModel)
        self.session.commit()
