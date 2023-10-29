import os

from rapidx.app.data.file.dicomfileimporter import DicomFileImporter
from rapidx.app.widgets.multifilesetmodeltreewidget import MultiFileSetModelTreeWidget

FILEMODELPATH = os.path.join(os.environ['HOME'], f'Desktop/downloads/dataset/scan1/image-00000.dcm')


def test_addMultiFileSetModelToMultiFileSetTreeWidget(session):
    importer = DicomFileImporter(path=FILEMODELPATH, session=session)
    importer.run()
    multiFileSetModel = importer.data()
    treeWidget = MultiFileSetModelTreeWidget()
    treeWidget.addData(multiFileSetModel)
    assert treeWidget.data()[0] == multiFileSetModel
