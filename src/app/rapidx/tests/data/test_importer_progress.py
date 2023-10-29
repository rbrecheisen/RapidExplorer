import os

from PySide6.QtCore import QThreadPool

from rapidx.app.data.importer import Importer


FILESETMODELNAME = 'myFileSet'
FILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1')

progress = 0


def test_importerSignalling(db, qtbot):
    importer = Importer(name=FILESETMODELNAME, path=FILESETMODELPATH, db=db)
    importer.signal().progress.connect(updateProgress)
    importer.signal().finished.connect(importFinished)
    with qtbot.waitSignals([importer.signal().progress, importer.signal().finished], timeout=1000):        
        QThreadPool.globalInstance().start(importer)

def updateProgress(value) -> None:
    global progress
    progress = value

def importFinished() -> None:
    assert progress == 100
