from rapidx.app.data.db.dbaddcommand import DbAddCommand
from rapidx.app.data.db.dbgetcommand import DbGetCommand
from rapidx.app.data.db.dbqueryallcommand import DbQueryAllCommand
from rapidx.app.data.db.dbfilterbycommand import DbFilterByCommand
from rapidx.app.data.db.dbupdatecommand import DbUpdateCommand
from rapidx.app.data.db.dbdeletecommand import DbDeleteCommand
from rapidx.app.data.file.filemodel import FileModel
from rapidx.app.data.fileset.filesetmodel import FileSetModel
from rapidx.app.data.multifileset.multifilesetmodel import MultiFileSetModel
from rapidx.app.data.file.filemodelfactory import FileModelFactory
from rapidx.app.data.fileset.filesetmodelfactory import FileSetModelFactory
from rapidx.app.data.multifileset.multifilesetmodelfactory import MultiFileSetModelFactory


def test_addCommand(db):
    multiFileSetModel = MultiFileSetModelFactory().create()
    fileSetModel = FileSetModelFactory().create(multiFileSetModel=multiFileSetModel)
    fileModel = FileModelFactory().create(fileSetModel=fileSetModel, path='/path/to/file')
    command = DbAddCommand(db, FileModel, fileModel)
    fileModel = command.execute()
    assert fileModel.id()


def test_getCommand(db):
    pass


def test_queryAllCommand(db):
    pass


def test_filterByCommand(db):
    pass


def test_updateCommand(db):
    pass


def test_deleteCommand(db):
    pass
