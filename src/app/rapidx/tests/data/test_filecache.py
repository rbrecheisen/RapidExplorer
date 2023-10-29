import os

from rapidx.app.data.filecache import FileCache
from rapidx.app.data.file.dicomfileimporter import DicomFileImporter


FILEMODELNAME = 'image-00000.dcm'
FILEMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1/{FILEMODELNAME}')


def test_importDicomFileAndCheckFileCacheAddRemoveAndClear(db):
    importer = DicomFileImporter(path=FILEMODELPATH, db=db)
    importer.run()
    # dicomFile = importer.data()
    multiFileSetModel = importer.data()
    # TODO: How do I get at the individual FileModel objects?
    
    # cache = FileCache()
    # assert cache.get(dicomFile.id())
    # cache.remove(dicomFile.id())
    # assert not cache.get(dicomFile.id())
    # cache.add(dicomFile)
    # cache.clear()
    # assert not cache.get(dicomFile.id())
