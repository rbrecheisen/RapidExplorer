import os

from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfileimporter import DicomFileImporter


FILEMODELNAME = 'image-00000.dcm'
FILEMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1/{FILEMODELNAME}')


def test_importDicomFileAndCheckInFileCache(session):
    importer = DicomFileImporter(path=FILEMODELPATH, session=session)
    importer.run()
    dicomFile = importer.data()
    assert dicomFile.id()
    assert dicomFile.data()
    assert dicomFile.header()
    assert dicomFile.header('SeriesDescription')
    assert dicomFile.pixelData().shape == (512, 512)
    fileModel = dicomFile.fileModel()
    assert fileModel.fileSetModel()
    assert fileModel.fileSetModel().name().startswith('fileset')
    assert fileModel.fileSetModel().multiFileSetModel()
    assert fileModel.fileSetModel().multiFileSetModel().name().startswith('multifileset')
    cache = FileCache()
    assert cache.get(dicomFile.id())
