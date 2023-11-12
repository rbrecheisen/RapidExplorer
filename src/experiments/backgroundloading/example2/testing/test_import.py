import os

import utils
from data.filecache import FileCache
from data.fileimporter import FileImporter
from data.filesetimporter import FileSetImporter
from data.multifilesetimporter import MultiFileSetImporter
from data.dicomfiletype import DicomFileType

MULTIFILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset')
FILESETPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1')
FILEPATH = os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm')


def test_FileImporter():
    importer = FileImporter(path=FILEPATH, fileType=DicomFileType)
    importer.run()
    cache = FileCache()
    assert cache.nrFiles() == 1
    firstKey = list(cache.data().keys())[0]
    file = cache.data()[firstKey]
    assert file.id
    cache.clear()


def test_FileSetImporter():
    importer = FileSetImporter(path=FILESETPATH, fileType=DicomFileType)
    importer.run()
    cache = FileCache()
    assert cache.nrFiles() == 361
    cache.clear()


def test_MultiFileSetImporter():
    importer = MultiFileSetImporter(path=MULTIFILESETPATH, fileType=DicomFileType)
    importer.run()
    cache = FileCache()
    assert cache.nrFiles() == 1083
    cache.clear()
