import os

from rapidx.tests.data.filecache import FileCache
from rapidx.tests.data.file.dicomfileimporter import DicomFileImporter


FILEMODELNAME = 'image-00000.dcm'
FILEMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1/{FILEMODELNAME}')


def test_importDicomFileAndCheckInFileCache(session):
    # Load single DICOM file, check it has the correct contents
    importer = DicomFileImporter(path=FILEMODELPATH, session=session)
    importer.execute()
    dicomFile = importer.data()
    assert dicomFile.id()
    assert dicomFile.data()
    assert dicomFile.header()
    assert dicomFile.header('SeriesDescription')
    assert dicomFile.pixelData().shape == (512, 512)
    # Check the file is associated with a properly embedded FileModel in a MultiFileSetModel
    fileModel = dicomFile.fileModel()
    assert fileModel.fileSetModel()
    assert fileModel.fileSetModel().name().startswith('fileset')
    assert fileModel.fileSetModel().multiFileSetModel()
    assert fileModel.fileSetModel().multiFileSetModel().name().startswith('multifileset')
    # Check file is also stored in file cache (more extensive testing of
    # file cache is done in test_filecache.py)
    cache = FileCache()
    assert cache.get(dicomFile.id())
