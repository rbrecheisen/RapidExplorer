import os
import pytest

from rapidx.app.data.filecache import FileCache
from rapidx.app.data.fileset.dicomfilesetimporter import DicomFileSetImporter


FILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1')


@pytest.mark.long_running
def test_importDicomFileSetCheckFileCacheClear(db):
    importer = DicomFileSetImporter(path=FILESETMODELPATH, db=db)
    importer.run()
    multiFileSetModel = importer.data()    
    cache = FileCache()
    fileModelId = None
    for fileSetModel in multiFileSetModel.fileSetModels:
        assert fileSetModel.id
        for fileModel in fileSetModel.fileModels:
            assert fileModel.id
            assert cache.get(fileModel.id)
            if not fileModelId:
                fileModelId = fileModel.id
    cache.clear()
    assert not cache.get(fileModelId)
