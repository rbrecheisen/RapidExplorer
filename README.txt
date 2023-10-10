DATASETS

I now have a DatasetBuilder that parses a directory structure searching for files of a certain type.
It's now doing DICOM files but it could be anything.

I now have several DICOM loaders. These loaders are passed a dataset object that lists the file paths.
This is a bit strange. The loader could find these file paths itself and then RETURN a dataset.

class Dataset:
    self.fileSets = []

class FileSet:
    self.files = []

class File:
    def getData():
        pass

class PngFile(File):
    def getData():
        return []

class DicomFile(File):
    def getData():
        return pydicom.FileDataset

pixels = dataset.getFileSet(0).getFile(0).getData() # in case of PngFile
     p = dataset.getFileSet(0).getFile(0).getData() # in case of DicomFile

TASKS

Tasks operate on datasets and produce datasets as output whether it be
a simple scalar value, a table or image dataset. Each task knows what
kind of dataset it supports as input and what kind of dataset it outputs.

class Task:
- input_dataset_type = DicomImageDataset
- output_dataset_type = ArrayDataset2D


VIEWS

Views display datasets.
