import os

from rapidx.app.data.fileset.dicomfilesetimporter import DicomFileSetImporter

FILESETMODELNAME = 'myFileSet'
FILESETMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1')


def test_addMultiFileSetModelToMultiFileSetTreeWidget(session):
    return
    importer = DicomFileSetImporter(name=FILESETMODELNAME, path=FILESETMODELPATH, session=session)
    importer.run()
    multiFileSetModel = importer.data()
    treeWidget = MultiFileSetTreeWidget()
    treeWidget.addData(multiFileSetModel)
    assert treeWidget
