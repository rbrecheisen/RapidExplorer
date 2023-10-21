from typing import Union, List

from rapidx.app.dataset import Dataset
from rapidx.app.fileset import FileSet
from rapidx.app.file import File
from rapidx.app.datasetmodel import DatasetModel
from rapidx.app.filesetmodel import FileSetModel
from rapidx.app.filemodel import FileModel
from rapidx.app.db import DbSession


class DatasetStorageManager:
    def __init__(self, session=None) -> None:
        self._session = session

    def save(self, dataObj: Union[Dataset, FileSet, File]) -> Union[Dataset, FileSet, File]:
        if isinstance(dataObj, Dataset):
            return self._saveDataset(dataset=dataObj)
        elif isinstance(dataObj, FileSet):
            return self._saveFileSet(fileSet=dataObj)
        elif isinstance(dataObj, File):
            return self._saveFile(file=dataObj)
        else:
            raise RuntimeError(f'Wrong data object type: {type(dataObj)}')
    
    def _saveDataset(self, dataset: Dataset) -> Dataset:
        with DbSession() as session:
            if self._session:
                session = self._session
            if not dataset.id():
                datasetModel = DatasetModel(path=dataset.path(), name=dataset.name())
                session.add(datasetModel)
                session.commit()
                dataset.setId(datasetModel.id)
            else:
                datasetModel = session.get(DatasetModel, dataset.id())
                datasetModel.name = dataset.name()
                datasetModel.path = dataset.path()
                session.commit()
            for fileSet in dataset.fileSets():
                fileSet.setDatasetId(datasetId=dataset.id())
                self._saveFileSet(fileSet=fileSet)
        return dataset

    def _saveFileSet(self, fileSet: FileSet) -> FileSet:
        with DbSession() as session:
            if self._session:
                session = self._session
            if not fileSet.id():
                datasetModel = session.get(DatasetModel, fileSet.datasetId())
                fileSetModel = FileSetModel(path=fileSet.path(), name=fileSet.name(), dataset=datasetModel)
                session.add(fileSetModel)
                session.commit()
                fileSet.setId(fileSetModel.id)
            else:
                fileSetModel = session.get(FileSetModel, fileSet.id())
                fileSetModel.path = fileSet.path()
                fileSetModel.name = fileSet.name()
                session.commit()
            for file in fileSet.files():
                file.setFileSetId(fileSetId=fileSet.id())
                self._saveFile(file=file)
        return fileSet

    def _saveFile(self, file: File) -> File:
        with DbSession() as session:
            if self._session:
                session = self._session
            if not file.id():
                fileSetModel = session.get(FileSetModel, file.fileSetId())
                fileModel = FileModel(path=file.path(), fileSet=fileSetModel)
                session.add(fileModel)
                session.commit()
                file.setId(fileModel.id)
            else:
                fileModel = session.get(FileModel, file.id())
                fileModel.path=file.path()
                session.commit()
        return file

    def load(self, datasetId: int) -> Dataset:
        # TODO: Support loading of Dataset, FileSet and File objects? Perhaps support load by ID as well?
        # Add it when you actually need it.
        with DbSession() as session:
            if self._session:
                session = self._session
            datasetModel = session.get(DatasetModel, datasetId)
            dataset = Dataset(path=datasetModel.path, name=datasetModel.name)
            dataset.setId(datasetModel.id)
            for fileSetModel in datasetModel.fileSets:
                fileSet = FileSet(path=fileSetModel.path, name=fileSetModel.name)  # What about DicomFileSet?
                fileSet.setDatasetId(datasetId=datasetId)
                fileSet.setId(fileSetModel.id)
                for fileModel in fileSetModel.files:
                    file = File(path=fileModel.path)  # Abstract type!
                    file.setFileSetId(fileSetId=fileSet.id())
                    file.setId(fileModel.id)
                    fileSet.files.append(file)
                dataset.fileSets.append(fileSet)
        return dataset
    
    def loadAll(self) -> List[Dataset]:
        with DbSession() as session:
            if self._session:
                session = self._session
            datasetModels = session.query(DatasetModel).all()
            datasets = []
            for datasetModel in datasetModels:
                dataset = self.load(datasetId=datasetModel.id)
                datasets.append(dataset)
        return datasets

    def delete(self, datasetId: int):
        # Support deleting Dataset, FileSet and File objects? For example, from a tree widget?
        # The physical underlying data is untouched
        with DbSession() as session:
            if self._session:
                session = self._session
            datasetModel = session.get(DatasetModel, datasetId)
            session.delete(datasetModel)