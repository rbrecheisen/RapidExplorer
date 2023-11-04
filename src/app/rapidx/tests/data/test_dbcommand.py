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


def assertIds(multiFileSetModel: MultiFileSetModel) -> None:
    assert multiFileSetModel.id()
    for fileSetModel in multiFileSetModel.fileSetModels():
        assert fileSetModel.id()
        for fileModel in fileSetModel.fileModels():
            assert fileModel.id()


def addMultiFileSetModelObject(db):
    multiFileSetModel = MultiFileSetModelFactory().create()
    fileSetModel1 = FileSetModelFactory().create(multiFileSetModel=multiFileSetModel, name='fileSetModel1')
    fileSetModel2 = FileSetModelFactory().create(multiFileSetModel=multiFileSetModel, name='fileSetModel2')
    fileModel11 = FileModelFactory().create(fileSetModel=fileSetModel1, path='/path/to/file11')
    fileModel12 = FileModelFactory().create(fileSetModel=fileSetModel1, path='/path/to/file12')
    fileModel21 = FileModelFactory().create(fileSetModel=fileSetModel2, path='/path/to/file21')
    fileModel22 = FileModelFactory().create(fileSetModel=fileSetModel2, path='/path/to/file22')
    multiFileSetModel = DbAddCommand(db, MultiFileSetModel, multiFileSetModel).execute()
    fileSetModel1 = DbAddCommand(db, FileSetModel, fileSetModel1).execute()
    fileSetModel1 = DbAddCommand(db, FileSetModel, fileSetModel1).execute()
    fileModel11 = DbAddCommand(db, FileModel, fileModel11).execute()
    fileModel12 = DbAddCommand(db, FileModel, fileModel12).execute()
    fileModel21 = DbAddCommand(db, FileModel, fileModel21).execute()
    fileModel22 = DbAddCommand(db, FileModel, fileModel22).execute()
    assertIds(multiFileSetModel)
    return multiFileSetModel.id()


def deleteMultiFileSetModelObject(db, multiFileSetModelId):
    assert DbDeleteCommand(db, MultiFileSetModel, multiFileSetModelId).execute()
    multiFileSetModel = DbGetCommand(db, MultiFileSetModel, multiFileSetModelId).execute()
    assert not multiFileSetModel


def test_getCommand(db):
    multiFileSetModelId = addMultiFileSetModelObject(db)
    multiFileSetModel = DbGetCommand(db, MultiFileSetModel, multiFileSetModelId).execute()
    assert multiFileSetModel.id() == multiFileSetModelId
    assertIds(multiFileSetModel)
    deleteMultiFileSetModelObject(db, multiFileSetModelId)


def test_queryAllCommand(db):
    multiFileSetModelId = addMultiFileSetModelObject(db)
    assert len(DbQueryAllCommand(db, FileModel).execute()) ==4
    assert len(DbQueryAllCommand(db, FileSetModel).execute()) == 2
    assert len(DbQueryAllCommand(db, MultiFileSetModel).execute()) == 1
    deleteMultiFileSetModelObject(db, multiFileSetModelId)


def test_filterByCommand(db):
    # multiFileSetModelId = addMultiFileSetModelObject(db)
    # assert len(DbFilterByCommand(db, FileModel, _path='/path/to/file11').execute()) == 1
    # deleteMultiFileSetModelObject(db, multiFileSetModelId)
    pass


def test_updateCommand(db):
    # Add object
    # Get it back
    # Update one of its fields
    # Get it back again and check change still there
    pass


def test_deleteCommand(db):
    # Add object
    # Get it back and check it's state
    # Delete object
    # Try to get it back and check nonexistence
    pass
