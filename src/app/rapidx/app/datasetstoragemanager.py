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
            # Create or update dataset model
            datasetModel = session.query(DatasetModel).filter_by(name=dataset.name()).first()
            if not datasetModel:
                datasetModel = DatasetModel(path=dataset.path(), name=dataset.name())
                session.add(datasetModel)
            else:
                datasetModel.name = dataset.name()
                datasetModel.path = dataset.path()
            # Create or update file sets
            for fileSet in dataset.fileSets():
                fileSetModel = session.query(FileSetModel).filter_by(name=fileSet.name()).first()
                if not fileSetModel:
                    fileSetModel = FileSetModel(path=fileSet.path(), name=fileSet.name(), dataset=datasetModel)
                    session.add(fileSetModel)
                else:
                    fileSetModel.path = fileSet.path()
                    fileSetModel.name = fileSet.name()
                # Create or update files
                for file in fileSet.files():
                    fileModel = session.query(FileModel).filter_by(path=file.path(), fileSet=fileSetModel).first()
                    if not fileModel:
                        fileModel = FileModel(path=file.path(), fileSet=fileSetModel)
                        session.add(fileModel)
                    else:
                        fileModel = path=file.path()
            session.commit()
        return dataset.name()

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