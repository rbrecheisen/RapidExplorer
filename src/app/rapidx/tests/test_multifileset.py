import os

from rapidx.tests.data.filecache import FileCache
from rapidx.tests.data.multifileset.dicommultifilesetimporter import DicomMultiFileSetImporter


MULTIFILESETMODELNAME = 'myMultiFileSet'
MULTIFILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset')


def test_importDicomMultiFileSetAndCheckInFileCache(session):
    importer = DicomMultiFileSetImporter(name=MULTIFILESETMODELNAME, path=MULTIFILESETMODELPATH, session=session)
    dicomFiles = importer.execute()
    assert dicomFiles
    assert len(dicomFiles) > 0
    assert len(dicomFiles[0]) > 0

    # dicomFiles = importer.data()
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
