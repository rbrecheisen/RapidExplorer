import os
import json
import shutil
import numpy as np
import nibabel as nib

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.data.filecontentcache import FileContentCache
from mosamaticdesktop.utils import readFromCache, writeToCache
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class NumPyToNiftiConverterTask(Task):
    def __init__(self) -> None:
        super(NumPyToNiftiConverterTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Converts 2D or 3D NumPy arrays to NIFTI format'
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set Name',
        )
        self.addTextParameter(
            name='transformationMatrix',
            labelText='Affine Transformation Matrix',
            optional=True,
        )
        self.addPathParameter(
            name='outputFileSetPath',
            labelText='Output File Set Path',
        )
        self.addTextParameter(
            name='outputFileSetName',
            labelText='Output File Set Name',
            optional=True,
        )
        self.addBooleanParameter(
            name='overwriteOutputFileSet',
            labelText='Overwrite Output File Set',
            defaultValue=True,
        )
        self._cache = FileContentCache()

    def convertNumPyToNifti(self, numpyArray, transformationMatrix=None):
        if transformationMatrix is None:
            transformationMatrix = np.eye(4)
        if numpyArray.ndim == 2:
            numpyArray = numpyArray[:, :, np.newaxis]
        niftiImage = nib.Nifti1Image(numpyArray, transformationMatrix, dtype='int64')
        return niftiImage

    def execute(self) -> None:

        # Prepare input parameters
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(inputFileSetName)
        transformationMatrix = None
        transformationMatrixString = self.parameter('transformationMatrix').value()
        if transformationMatrixString and transformationMatrixString != '':
            try:
                transformationMatrix = json.loads(transformationMatrixString)
                transformationMatrix = np.array(transformationMatrix)
            except json.JSONDecodeError as e:
                self.addError(f'Could not load transformation matrix from parameter {transformationMatrixString} ({e})', cancel=True)

        # Prepare output parameters
        outputFileSetPath = self.parameter('outputFileSetPath').value()
        outputFileSetName = self.parameter('outputFileSetName').value()
        if outputFileSetName is None:
            outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
        overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        if overwriteOutputFileSet:
            if os.path.isdir(outputFileSetPath):
                shutil.rmtree(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=True)

        step = 0
        files = inputFileSet.files()
        nrSteps = len(files)
        for file in files:

            # Chec if the task should cancel
            if self.statusIsCanceled():
                self.addInfo('Canceling task...')
                break

            if not file.name().endswith('.npy'):
                self.addWarning(f'Skipping non-NumPy file {file.name()}...')
                self.updateProgress(step=step, nrSteps=nrSteps)
                step += 1
                continue
            
            try:
                # Try to load file content from cache first. If it's not available
                # read it from disk
                content = readFromCache(file=file)
                if not content:
                    numpyArray = np.load(file.path())
                    content = writeToCache(file, numpyArray)
                numpyArray = content.fileObject()
                # Buid output file path
                outputFileName = file.name()[:-4] + '.nii.gz'
                outputFilePath = os.path.join(outputFileSetPath, outputFileName)
                # Convert NumPy array to NIFTI format and save
                niftiImage = self.convertNumPyToNifti(numpyArray=numpyArray, transformationMatrix=transformationMatrix)
                niftiImage.to_filename(outputFilePath)
            except OSError:
                self.addError(f'Could not load NumPy array from file: {file.path()}')

            # Update progress for this iteration         
            self.updateProgress(step=step, nrSteps=nrSteps)
            step += 1

        # Finalize task
        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
        self.addInfo('Finished')