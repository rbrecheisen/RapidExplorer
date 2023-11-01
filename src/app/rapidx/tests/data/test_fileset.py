import os
import pytest

from rapidx.app.data.filecache import FileCache
from rapidx.app.data.fileset.dicomfilesetimporter import DicomFileSetImporter


FILESETMODELNAME = 'myFileSet'
FILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1')


@pytest.mark.long_running
def test_importDicomFileSetAndCheckInFileCache(db):
    importer = DicomFileSetImporter(path=FILESETMODELPATH, db=db)
    importer.run()
    # dicomFiles = importer.data()
    multiFileSetModel = importer.data()
    # TODO: How do I get at the individual FileModel objects?
    
    # assert isinstance(dicomFiles, list)
    # assert len(dicomFiles) > 0
    # for dicomFile in dicomFiles:
    #     assert dicomFile.id()
    #     assert dicomFile.data()
    #     assert dicomFile.header()
    #     assert dicomFile.header(attributeName='SeriesDescription')
    #     assert dicomFile.pixelData().shape == (512, 512)
    #     # Check model associations
    #     assert dicomFile.fileModel().fileSetModel()
    #     assert dicomFile.fileModel().fileSetModel().name() == FILESETMODELNAME
    #     assert dicomFile.fileModel().fileSetModel().multiFileSetModel()
    #     assert dicomFile.fileModel().fileSetModel().multiFileSetModel().name().startswith('multifileset')
    #     cache = FileCache()
    #     assert cache.get(dicomFile.id())