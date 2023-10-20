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
            if not dataset.id():
                datasetModel = DatasetModel(path=dataset.path(), name=dataset.name())
                session.add(datasetModel)
                session.commit()
                dataset.setId(datasetModel.id)
            else:
                datasetModel = session.get(DatasetModel, dataset.id())  # ERROR!
                datasetModel.name = dataset.name()
                datasetModel.path = dataset.path()
                session.commit()
            for fileSet in dataset.fileSets():
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
                    if not file.id():
                        fileModel = FileModel(path=file.path(), fileSet=fileSetModel)
                        session.add(fileModel)
                        session.commit()
                        file.setId(fileModel.id)
                    else:
                        fileModel = session.get(FileModel, file.id())
                        fileModel.path=file.path()
                        session.commit()
        return dataset

    def load(self, name: str):
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
        with DbSession() as session:
            datasetModel = session.query(DatasetModel).filter_by(name=name).one()
            session.delete(datasetModel)