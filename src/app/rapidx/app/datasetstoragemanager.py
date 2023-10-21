from typing import Union

from rapidx.app.dataset import Dataset
from rapidx.app.fileset import FileSet
from rapidx.app.file import File
from rapidx.app.datasetmodel import DatasetModel
from rapidx.app.filesetmodel import FileSetModel
from rapidx.app.filemodel import FileModel
from rapidx.app.db import DbSession


class DatasetStorageManager:
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
                self._saveFileSet(fileSet, session)
        return dataset

    def _saveFileSet(self, fileSet: FileSet) -> FileSet:
        with DbSession() as session:
            if not fileSet.id():
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
                self._saveFile(file)
        return fileSet

    def _saveFile(self, file: File) -> File:
        with DbSession() as session:
            if not file.id():
                fileModel = FileModel(path=file.path(), fileSet=fileSetModel)
                session.add(fileModel)
                session.commit()
                file.setId(fileModel.id)
            else:
                fileModel = session.get(FileModel, file.id())
                fileModel.path=file.path()
                session.commit()
        return file

    def load(self, name: str):
        # TODO: Support loading of Dataset, FileSet and File objects? Perhaps support load by ID as well?
        # Add it when you actually need it.
        with DbSession() as session:
            datasetModel = session.query(DatasetModel).filter_by(name=name).one()
            dataset = Dataset(path=datasetModel.path, name=datasetModel.name)
            dataset.setId(datasetModel.id)
            for fileSetModel in datasetModel.fileSets:
                fileSet = FileSet(path=fileSetModel.path, name=fileSetModel.name)
                fileSet.setId(fileSetModel.id)
                for fileModel in fileSetModel.files:
                    file = File(path=fileModel.path)
                    file.setId(fileModel.id)
                    fileSet.files.append(file)
                dataset.fileSets.append(fileSet)
        return dataset

    def delete(self, name: str):
        # Support deleting Dataset, FileSet and File objects? For example, from a tree widget?
        # The physical underlying data is untouched
        with DbSession() as session:
            datasetModel = session.query(DatasetModel).filter_by(name=name).one()
            session.delete(datasetModel)