import os

from PySide6.QtCore import QThreadPool

# from rapidx.app.data.multifileset.dicommultifilesetfactory import DicomMultiFileSetFactory
from rapidx.app.data.multifileset.dicommultifilesetimporter import DicomMultiFileSetImporter

# MULTIFILESETMODELNAME = 'myMultiFileSet'
MULTIFILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset')


def test_dicomMultiFileSetImporterProgressSignalling(db, qtbot):
    """ This test should ensure that the importer sends out progress signals that
    have the correct value. Question is, how to do that? Progress should indicate
    how many files have been loaded out of the total number of files. 

    The code below doesn't work because of SQLite's single threading restriction. 
    TODO: Build a separate thread for SQLite operations that the other threads
    queue their database requests in.
    """
    def updateProgress(value):
        assert False

    def importFinished():
        assert False

    progress = 0
    importer = DicomMultiFileSetImporter(path=MULTIFILESETMODELPATH, db=db)
    importer.signal().progress.connect(updateProgress)
    importer.signal().finished.connect(importFinished)
    with qtbot.waitSignals([importer.signal().progress, importer.signal().finished], timeout=1000):        
        QThreadPool.globalInstance().start(importer)
