import os

from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfileimporter import DicomFileImporter


FILEMODELNAME = 'image-00000.dcm'
FILEMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1/{FILEMODELNAME}')


def test_importDicomFileAndCheckFileCacheAddRemoveAndClear(session):
    importer = DicomFileImporter(path=FILEMODELPATH, session=session)
    importer.execute()
    dicomFile = importer.data()
    cache = FileCache()
    assert cache.get(dicomFile.id())
    cache.remove(dicomFile.id())
    assert not cache.get(dicomFile.id())
    cache.add(dicomFile)
    cache.clear()
    assert not cache.get(dicomFile.id())
