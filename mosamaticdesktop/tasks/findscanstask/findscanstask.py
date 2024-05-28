import os
import shutil
import pydicom
import pydicom.errors

from typing import List
from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class FindScansTask(Task):
    def __init__(self) -> None:
        super(FindScansTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Searches for scans in root directory'
        )
        self.addPathParameter(
            name='rootDirectoryPath',
            labelText='Root Directory Path',
        )
        self.addBooleanParameter(
            name='rootDirectoryContainsSubjectDirectories',
            labelText='Root Directory Contains Subject Directories',
            defaultValue=True,
        )        
        self.addOptionGroupParameter(
            name='orientation',
            labelText='Orientation',
            options=['AXIAL', 'SAGITTAL', 'CORONAL'],
            defaultValue='AXIAL',
        )
        self.addPathParameter(
            name='outputDirectoryPath',
            labelText='Output Directory Path For Scans',
        )
        self.addBooleanParameter(
            name='overwriteOutputDirectory',
            labelText='Overwrite Output Directory',
            defaultValue=True,
        )

    def isDicomFile(self, fPath) -> bool:
        try:
            pydicom.dcmread(fPath, stop_before_pixels=True)
            return True
        except pydicom.errors.InvalidDicomError:
            return False
        
    def dicomFileHasSeriesInstanceUID(self, fPath) -> bool:
        if self.isDicomFile(fPath):
            if 'SeriesInstanceUID' in pydicom.dcmread(fPath, stop_before_pixels=True):
                return True
        return False
        
    def getOrientation(self, fPath) -> str:
        p = pydicom.dcmread(fPath, stop_before_pixels=True)
        if p.ImageOrientationPatient is not None and len(p.ImageOrientationPatient) == 6:
            axial = [1, 0, 0, 0, 1, 0]
            sagittal = [0, 1, 0, 0, 0, -1]
            coronal = [1, 0, 0, 0, 0, -1]
            # Normalize for floating-point imprecisions
            if all(abs(o - a) < 0.1 for o, a in zip(p.ImageOrientationPatient, axial)):
                return 'AXIAL'
            elif all(abs(o - s) < 0.1 for o, s in zip(p.ImageOrientationPatient, sagittal)):
                return 'SAGITTAL'
            elif all(abs(o - c) < 0.1 for o, c in zip(p.ImageOrientationPatient, coronal)):
                return 'CORONAL'
        return 'Unknown orientation'
        
    def loadScans(self, directory, orientation) -> List[str]:
        scans = {}
        for root, dirs, files in os.walk(directory):
            for f in files:
                fPath = os.path.join(root, f)
                if self.dicomFileHasSeriesInstanceUID(fPath) and self.getOrientation(fPath) == orientation:
                    p = pydicom.dcmread(fPath, stop_before_pixels=True)
                    if p.SeriesInstanceUID not in scans.keys():
                        scans[p.SeriesInstanceUID] = []
                    scans[p.SeriesInstanceUID].append(fPath)
        return scans
    
    def saveScans(self, scans, directory, subjectName=None) -> None:
        scanNr = 0
        for key in scans.keys():
            if subjectName:
                scanName = '{}-scan-{:02d}'.format(subjectName, scanNr)
            else:
                scanName = 'scan-{:02d}'.format(scanNr)
            filePath = scans[key]
            fileName = os.path.split(filePath)[1]
            os.makedirs(os.path.join(directory, scanName), exist_ok=True)
            shutil.copy(filePath, os.path.join(directory, scanName, fileName))
            scanNr += 1

    def execute(self) -> None:
        rootDirectoryPath = self.parameter('rootDirectoryPath').value()
        rootDirectoryContainsSubjectDirectories = self.parameter('rootDirectoryContainsSubjectDirectories').value()
        orientation = self.parameter('orientation').value()
        outputDirectoryPath = self.parameter('outputDirectoryPath').value()
        overwriteOutputDirectory = self.parameter('overwriteOutputDirectory').value()
        if overwriteOutputDirectory:
            if os.path.isdir(outputDirectoryPath):
                shutil.rmtree(outputDirectoryPath)
        os.makedirs(outputDirectoryPath, exist_ok=True)

        if rootDirectoryContainsSubjectDirectories:
            for subjectName in os.listdir(rootDirectoryPath):
                subjectDirPath = os.path.join(rootDirectoryPath, subjectName)
                if os.path.isdir(subjectDirPath):
                    scans = self.loadScans(subjectDirPath, orientation)
                    self.saveScans(scans, outputDirectoryPath, subjectName)
        else:
            scans = self.loadScans(rootDirectoryPath, orientation)
            self.saveScans(scans, outputDirectoryPath)