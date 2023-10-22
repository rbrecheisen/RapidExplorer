import pydicom

from rapidx.tests.data.filemodel import FileModel


class DicomFile:
    """ Represents a physical DICOM file with binary content 
    """
    def __init__(self, data: pydicom.FileDataset, fileModel: FileModel) -> None:
        self.data = data
        self.fileModel = fileModel

    