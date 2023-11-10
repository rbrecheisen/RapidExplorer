import pytest


""" 
This testcase tests 3 scenario's:

    (1) Files not in SQL and not in cache
    (2) Files in SQL but not in cache

Scenario 1:
We start with a goal: importing a file, fileset or multi-fileset. Let's say we want
to import a single DICOM file. We have a path to this file

DicomFileImporter:
    def run(path):
        fileModel = createFileModel(path)               # File model now in SQL
        dicomFile = loadDicomFileFromModel(fileModel)   # File contents have now been loaded
        FileCache().add(dicomFile)                      # File is now in cache

DicomFileSetImporter:
    def run(path):
        fileSetModel = createFileSetModel(path)
        dicomFileSet = loadDicomFileSetFromModel(fileSetModel)
        cache = FileCache()
        for dicomFile in dicomFileSet.files():
            cache.add(dicomFile)

DicomMultiFileSetImporter:
    def run(path):
        multiFileSetModel = createFileSetModel(path)
        dicomMultiFileSet = loadDicomMultiFileSetModel(multiFileSetModel)
        cache = FileCache()
        for dicomFileSet in dicomMultiFileSet.fileSets():
            for dicomFile in dicomFileSet.files():
                cache.add(dicomFile)
"""