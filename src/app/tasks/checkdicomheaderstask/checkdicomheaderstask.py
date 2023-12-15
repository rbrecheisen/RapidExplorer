import os
import shutil
import pydicom
import pydicom.errors

from tasks.task import Task
from tasks.tasksignal import TaskSignal
from tasks.taskoutput import TaskOutput
from data.fileset import FileSet
from settings.settinglabel import SettingLabel
from settings.settingfileset import SettingFileSet
from settings.settinginteger import SettingInteger
from settings.settingfilesetpath import SettingFileSetPath
from settings.settingboolean import SettingBoolean
from settings.settingtext import SettingText
from logger import Logger

LOGGER = Logger()

DESCRIPTION = """
This task checks DICOM headers to see whether all attributes are correct for MuscleFatSegmentationTask
"""


class CheckDicomHeadersTask(Task):
    NAME = 'CheckDicomHeadersTask'
    
    def __init__(self) -> None:
        super(CheckDicomHeadersTask, self).__init__()
        self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
        self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
        self.settings().add(SettingText(name='requiredDicomAttributes', displayName='Required Attributes (comma-separated list)', defaultValue='Rows,Columns,PixelSpacing'))
        self.settings().add(SettingInteger(name='requiredNumberOfRows', displayName='Required Number of Rows', minimum=0, maximum=1024, defaultValue=512))
        self.settings().add(SettingInteger(name='requiredNumberOfColumns', displayName='Required Number of Columns', minimum=0, maximum=1024, defaultValue=512))
        self.settings().add(SettingBoolean(name='copyNonDicomFilesToOutputFileSet', displayName='Copy Non-DICOM Files to Output File Set', defaultValue=False))
        self.settings().add(SettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
        self.settings().add(SettingText(name='outputFileSetName', displayName='Output File Set Name', optional=True))
        self.settings().add(SettingBoolean(name='overwriteOutputFileSet', displayName='Overwrite Output File Set', defaultValue=True))
        self._signal = TaskSignal()

    def signal(self) -> TaskSignal:
        return self._signal

    def run(self) -> TaskOutput:
        # Get input file set
        dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
        dicomFileSet = self.dataManager().fileSetByName(name=dicomFileSetName)
        # Check DICOM files
        requiredDicomAttributes = self.settings().setting(name='requiredDicomAttributes').value()
        requiredDicomAttributes = [x.strip() for x in requiredDicomAttributes.split(',')]
        requiredNumberOfRows = self.settings().setting(name='requiredNumberOfRows').value()
        requiredNumberOfColumns = self.settings().setting(name='requiredNumberOfColumns').value()
        dicomFilesOk = []
        nonDicomFilesToIgnore = []
        errorInfo = []
        for dicomFile in dicomFileSet.files():
            try:
                p = pydicom.dcmread(dicomFile.path())
                p.decompress()
                allAttributesPresent = True
                for requiredAttribute in requiredDicomAttributes:
                    if requiredAttribute not in p:
                        errorInfo.append(f'{dicomFile.path()}: attribute {requiredAttribute} missing')
                        allAttributesPresent = False
                if not allAttributesPresent:
                    continue
                rowsAndColumnsOk = True
                if p.Rows != requiredNumberOfRows:
                    errorInfo.append(f'{dicomFile.path()}: rows={p.Rows} (should be {requiredNumberOfRows})')
                    rowsAndColumnsOk = False
                if p.Columns != requiredNumberOfColumns:
                    errorInfo.append(f'{dicomFile.path()}: columns={p.Columns} (should be {requiredNumberOfColumns})')
                if not rowsAndColumnsOk:
                    continue
                dicomFilesOk.append(dicomFile)
            except pydicom.errors.InvalidDicomError:
                nonDicomFilesToIgnore.append(dicomFile.path())
        # Build output file set
        outputFileSetPath = self.settings().setting(name='outputFileSetPath').value()
        outputFileSetName = self.settings().setting(name='outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = dicomFileSet.name() + '-checked'
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        overwriteOutputFileSet = self.settings().setting(name='overwriteOutputFileSet').value()
        if overwriteOutputFileSet:
            if os.path.isdir(outputFileSetPath):
                shutil.rmtree(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=False)
        LOGGER.info(f'CheckDicomHeadersTask.run() outputFileSetPath={outputFileSetPath}')
        # Copy files to output file set
        for dicomFile in dicomFilesOk:
            shutil.copy(dicomFile.path(), outputFileSetPath)
        # If enabled, copy non-DICOM files to output file set as well
        copyNonDicomFilesToOutputFileSet = self.settings().setting(name='copyNonDicomFilesToOutputFileSet').value()
        if copyNonDicomFilesToOutputFileSet:
            for dicomFile in nonDicomFilesToIgnore:
                shutil.copy(dicomFile.path(), outputFileSetPath)
        # Reload output file set        
        outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath)
        # Build task output and notify listeners
        taskOutput = TaskOutput(fileSet=outputFileSet, errorInfo=errorInfo)
        self.signal().finished.emit(taskOutput)
        return taskOutput


# class CheckDicomHeadersTask(Task):
#     NAME = 'CheckDicomHeadersTask'
    
#     def __init__(self) -> None:
#         super(CheckDicomHeadersTask, self).__init__()
#         self.settings().add(SettingLabel(name='description', value=DESCRIPTION))
#         self.settings().add(SettingFileSet(name='dicomFileSetName', displayName='DICOM File Set'))
#         self.settings().add(SettingText(name='requiredAttributes', displayName='Required Attributes (comma-separated list)', defaultValue='Rows,Columns,PixelSpacing'))
#         self.settings().add(SettingInteger(name='requiredNumberOfRows', displayName='Required Number of Rows', minimum=0, maximum=1024, defaultValue=512))
#         self.settings().add(SettingInteger(name='requiredNumberOfColumns', displayName='Required Number of Columns', minimum=0, maximum=1024, defaultValue=512))
#         self.settings().add(SettingBoolean(name='copyNonDicomFilesToOutputFileSet', displayName='Copy Non-DICOM Files to Output File Set', defaultValue=False))
#         self.settings().add(SettingBoolean(name='overwriteOutputFileSet', displayName='Overwrite Output File Set', defaultValue=True))
#         self.settings().add(SettingFileSetPath(name='outputFileSetPath', displayName='Output File Set Path'))
#         self._signal = TaskSignal()

#     def signal(self) -> TaskSignal:
#         return self._signal

#     def run(self) -> FileSet:
#         dicomFileSetName = self.settings().setting(name='dicomFileSetName').value()
#         dicomFileSet = self.dataManager().fileSetByName(name=dicomFileSetName)
#         dicomFilesCheckedOk = []
#         nonDicomFiles = []
#         errors = []
#         for dicomFile in dicomFileSet.files():
#             try:
#                 p = pydicom.dcmread(dicomFile.path())
#                 p.decompress()
#                 # Check required attributes
#                 requiredAttributes = self.settings().setting(name='requiredAttributes').value()
#                 requiredAttributes = [x.strip() for x in requiredAttributes.split(',')]
#                 allAttributesPresent = True
#                 for requiredAttribute in requiredAttributes:
#                     if requiredAttribute not in p:
#                         errors.append(f'{dicomFile.path} does not contain attribute {requiredAttribute}')
#                     allAttributesPresent = False
#                 if not allAttributesPresent:
#                     continue
#                 # Check required number of rows and columns
#                 correctNumberOfRows = True
#                 requiredNumberOfRows = self.settings().setting(name='requiredNumberOfRows').value()
#                 if p.Rows != requiredNumberOfRows:
#                     errors.append(f'{dicomFile.path()} has wrong number of rows: {p.Rows} instead of {requiredNumberOfRows}')
#                     correctNumberOfRows = False
#                 correctNumberOfColumns = True
#                 requiredNumberOfColumns = self.settings().setting(name='requiredNumberOfColumns').value()
#                 if p.Columns != requiredNumberOfColumns:
#                     errors.append(f'{dicomFile.path()} has wrong number of columns: {p.Columns} instead of {requiredNumberOfColumns}')
#                     correctNumberOfColumns = False
#                 if not correctNumberOfRows or not correctNumberOfColumns:
#                     continue
#                 # All is well, add to checked list
#                 dicomFilesCheckedOk.append(dicomFile.path())
#             except pydicom.errors.InvalidDicomError:
#                 nonDicomFiles.append(dicomFile.path())
#         # Build output file set
#         outputFileSetPath = self.settings().setting(name='outputFileSetPath').value()
#         outputFileSetName = dicomFileSet.name() + '-checked'
#         outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
#         overwriteOutputFileSet = self.settings().setting(name='overwriteOutputFileSet').value()
#         LOGGER.info(f'overwriteOutputFileSet: {overwriteOutputFileSet}')
#         if overwriteOutputFileSet:
#             shutil.rmtree(outputFileSetPath)
#         os.makedirs(outputFileSetPath, exist_ok=False)
#         # Write error file if there were errors
#         if len(errors) > 0:
#             with open(os.path.join(outputFileSetPath, 'errors.txt'), 'w') as f:
#                 for error in errors:
#                     f.write(error + '\n')
#         # Write DICOM files that checked out ok
#         for dicomFile in dicomFilesCheckedOk:
#             shutil.copy(dicomFile, outputFileSetPath)
#         copyNonDicomFilesToOutputFileSet = self.settings().setting(name='copyNonDicomFilesToOutputFileSet').value()
#         if copyNonDicomFilesToOutputFileSet:
#             for file in nonDicomFiles:
#                 shutil.copy(file, outputFileSetPath)
#         # Load new output file set
#         outputFileSet = self.dataManager().importFileSet(fileSetPath=outputFileSetPath)
#         self.signal().finished.emit(outputFileSet)
#         return outputFileSet
