import os

from PySide6.QtCore import QThreadPool

from rapidx.app.data.fileset.dicomfilesetimporter import DicomFileSetImporter


FILESETMODELNAME = 'myFileSet'
FILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1')

progress = 0


def test_progessDicomFileSetImpoter(session, qtbot):
    importer = DicomFileSetImporter(name=FILESETMODELNAME, path=FILESETMODELPATH, session=session)
    importer.signal().progress.connect(updateProgress)
    importer.signal().finished.connect(importFinished)
    with qtbot.waitSignal(importer.signal().finished, timeout=1000):        
        QThreadPool.globalInstance().start(importer)

def updateProgress(value) -> None:
    global progress
    progress = value

def importFinished() -> None:
    assert progress == 100
