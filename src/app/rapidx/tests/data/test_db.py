from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.file.filemodelfactory import FileModelFactory
from rapidx.app.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.app.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory
from rapidx.app.data.db.dbinsertcommand import DbInsertCommand


def test_db(db):
    multiFileSetModel = MultiFileSetModelFactory.create()
    fileSetModel = FileSetModelFactory.create(multiFileSetModel)    
    fileModel = FileModelFactory.create(fileSetModel, path='/path/to/file')
    command = DbInsertCommand(db, FileModel, fileModel)
    fileModel = command.execute()
    assert fileModel.id()