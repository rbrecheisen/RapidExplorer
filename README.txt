DATASETS

Package structure:

- data
  - loaders
    - dicomdatasetloader.py
    - dicomfileloader.py
    - dicomfilesetloader.py
    - niftifileloader.py
    - pngfileloader.py
    - textfileloader.py
  - models
    - basemodel.py
    - datasetmodel.py
    - filemodel.py
    - filesetmodel.py
  - objs
    - dataset.py
    - file.py
    - fileset.py
- images
  - icons
- widgets
  - dialogs
    - logdialog.py
  - panels
    - taskpanel.py
  - datasetdockwidget.py
  - dockwidget.py
  - taskdockwidget.py
  - viewdockwidget.py


Dataset class structure and example code:

import os
import pydicom
from typing import List, Any
from abc import ABC, abstractmethod

class File(ABC):
    def __init__(self, path: str) -> None:
        self._path = path

    @abstractmethod
    def data(self) -> Any:
        pass

class FileSet:
    def __init__(self, path) -> None:
        self._path = path
        self._files = []

    def files(self) -> List(File):
        return self._files

    def addFile(self, f: File) -> None:
        self._files.append(f)  # Allows different types

class Dataset:
    def __init__(self, path) -> None:
        self._path = path
        self._fileSets = []

    def fileSets(self) -> List[FileSet]:
        return self._fileSets

    def addFileSet(self, fileSet: FileSet) -> None:
        self._fileSets.append(fileSet)

class DicomFile(File):
    def __init__(self, path) -> None:
        super(DicomFile, self).__init__(path)
        self._p = pydicom.dcmread(self._path)

    def data(self):
        return self._p

class TextFile(File):
    def __init__(self, path) -> None:
        super(TextFile, self).__init__(path)
        self._fileObj = open(self._path, 'r')

    def data(self):
        return self._fileObj
    

f = DicomFile(os.path.join(os.environ['HOME'], 'Desktop/downloads/dataset/scan1/image-00000.dcm'))
print(f.data())

f = TextFile(os.path.join(os.environ['HOME'], 'Desktop/downloads/file.txt'))
print(f.data().readline())

TASKS

Tasks operate on datasets and produce datasets as output whether it be
a simple scalar value, a table or image dataset. Each task knows what
kind of dataset it supports as input and what kind of dataset it outputs.

class Task:
- input_dataset_type = DicomImageDataset
- output_dataset_type = ArrayDataset2D


VIEWS

Views display datasets.
