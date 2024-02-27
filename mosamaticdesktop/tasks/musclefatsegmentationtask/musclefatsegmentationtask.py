import os
import json
import shutil
import zipfile
import pydicom
import pydicom.errors
import numpy as np

from typing import List, Any

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.tasks.musclefatsegmentationtask.tensorflowmodel import TensorFlowModel
from mosamaticdesktop.data.file import File
from mosamaticdesktop.logger import Logger
from mosamaticdesktop.utils import getPixelsFromDicomObject, convertLabelsTo157
from mosamaticdesktop.utils import normalizeBetween, Configuration
from mosamaticdesktop.utils import readFromCache, writeToCache

LOGGER = Logger()


class MuscleFatSegmentationTask(Task):
    ARGMAX = 0
    PROBABILITIES = 1

    def __init__(self) -> None:
        super(MuscleFatSegmentationTask, self).__init__()        
        self.addDescriptionParameter(
            name='description',
            description='Extract muscle and fat regions from L3 images'
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set',
        )
        self.addFileSetParameter(
            name='tensorFlowModelFileSetName',
            labelText='TensorFlow Model File Set',
        )
        self.addOptionGroupParameter(
            name='mode',
            labelText='Mode',
            defaultValue='ARGMAX',
            options=['ARGMAX', 'PROBABILITIES'],
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

    def loadModelFiles(self, files: List[File]) -> List[Any]:
        tfLoaded = False
        configuration = Configuration()
        for file in files:
            if file.name() == 'model.zip':
                content = readFromCache(file=file)
                if not content:
                    if not tfLoaded:
                        import tensorflow as tf # Only load TensorFlow package if necessary (takes some time)
                        tfLoaded = True
                    tensorFlowModelFileDirectory = configuration.taskConfigSubDirectory(taskName=__class__.__name__, dirName='tensorFlowModelFiles')
                    with zipfile.ZipFile(file.path()) as zipObj:
                        zipObj.extractall(path=tensorFlowModelFileDirectory)
                    tensorFlowModel = TensorFlowModel()
                    tensorFlowModel.load(modelFilePath=tensorFlowModelFileDirectory)
                    content = writeToCache(file=file, fileObject=tensorFlowModel)
                tensorFlowModel = content.fileObject()
            elif file.name() == 'contour_model.zip':
                content = readFromCache(file=file)
                if not content:
                    if not tfLoaded:
                        import tensorflow as tf # Only load TensorFlow package if necessary (takes some time)
                        tfLoaded = True
                    tensorFlowModelFileDirectory = configuration.taskConfigSubDirectory(taskName=__class__.__name__, dirName='tensorFlowModelFiles')
                    with zipfile.ZipFile(file.path()) as zipObj:
                        zipObj.extractall(path=tensorFlowModelFileDirectory)
                    tensorFlowContourModel = TensorFlowModel()
                    tensorFlowContourModel.load(modelFilePath=tensorFlowModelFileDirectory)
                    content = writeToCache(file=file, fileObject=tensorFlowContourModel)
                tensorFlowContourModel = content.fileObject()
            elif file.name() == 'params.json':
                content = readFromCache(file=file)
                if not content:
                    with open(file.path(), 'r') as f:
                        parameters = json.load(f)
                        content = writeToCache(file=file, fileObject=parameters)
                parameters = content.fileObject()
            else:
                pass
        return [tensorFlowModel, tensorFlowContourModel, parameters]

    def predictContour(self, contourModel, sourceImage, parameters):
        ct = np.copy(sourceImage)
        ct = normalizeBetween(ct, parameters['min_bound_contour'], parameters['max_bound_contour'])
        img2 = np.expand_dims(ct, 0)
        img2 = np.expand_dims(img2, -1)
        pred = contourModel.predict([img2])
        predSqueeze = np.squeeze(pred)
        pred_max = predSqueeze.argmax(axis=-1)
        mask = np.uint8(pred_max)
        return mask
    
    def execute(self) -> None:

        # Get input fileset
        inputFileSetName = self.parameter('inputFileSetName').value()
        inputFileSet = self.dataManager().fileSetByName(name=inputFileSetName)
        tensorFlowModelFileSetName = self.parameter('tensorFlowModelFileSetName').value()
        tensorFlowModelFileSet = self.dataManager().fileSetByName(tensorFlowModelFileSetName)
        # Setup output fileset path
        outputFileSetName = self.parameter('outputFileSetName').value()
        if outputFileSetName is None:
            outputFileSetName = self.generateTimestampForFileSetName(name=inputFileSetName)
        outputFileSetPath = self.parameter('outputFileSetPath').value()
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)

        overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
        self.addInfo(f'Overwrite output fileset: {overwriteOutputFileSet}')
        if overwriteOutputFileSet:
            if os.path.isdir(outputFileSetPath):
                shutil.rmtree(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=True)
        self.addInfo(f'Output fileset path: {outputFileSetPath}')

        # Get mode (ARGMAX or PROBABILITIES)
        modeText = self.parameter('mode').value()
        mode = MuscleFatSegmentationTask.ARGMAX if modeText == 'ARGMAX' else MuscleFatSegmentationTask.PROBABILITIES
        self.addInfo(f'Mode: {modeText}')

        # Load TensorFlow model files
        model, contourModel, parameters = self.loadModelFiles(files=tensorFlowModelFileSet.files())
        if model and parameters:

            # Start iterating of the files
            step = 0
            files = inputFileSet.files()
            segmentationFiles = []
            nrSteps = len(files)
            for file in files:

                # Check if task was canceled first
                if self.statusIsCanceled():
                    self.addInfo('Canceling task...')
                    break

                try:
                    # Read DICOM file (from cache first) and decompress if needed
                    content = readFromCache(file=file)
                    if not content:
                        p = pydicom.dcmread(file.path())
                        p.decompress()
                        content = writeToCache(file, p)
                    p = content.fileObject()

                    # Get pixels from DICOM file and normalize to positive range
                    img1 = getPixelsFromDicomObject(p, normalize=True)

                    # If contour model provided, apply it to detect abdominal contour
                    if contourModel:
                        mask = self.predictContour(contourModel=contourModel, sourceImage=img1, parameters=parameters)
                        img1 = normalizeBetween(img=img1, minBound=parameters['min_bound'], maxBound=parameters['max_bound'])
                        img1 = img1 * mask
                    else:
                        img1 = normalizeBetween(img=img1, minBound=parameters['min_bound'], maxBound=parameters['max_bound'])

                    img1 = img1.astype(np.float32)
                    img2 = np.expand_dims(img1, 0)
                    img2 = np.expand_dims(img2, -1)
                    pred = model.predict([img2]) ##### Move to separate AI class!
                    predSqueeze = np.squeeze(pred)

                    # Generate predicted output. Can be ARGMAX (pixel value with maximum probability) or
                    # PROBABILITIES, i.e, the individual class probabilities (muscle, SAT and VAT) in 
                    # each pixel
                    if mode == MuscleFatSegmentationTask.ARGMAX:
                        predMax = predSqueeze.argmax(axis=-1)
                        predMax = convertLabelsTo157(labelImage=predMax)
                        segmentationFile = os.path.join(outputFileSetPath, f'{file.name()}.seg.npy')
                        segmentationFiles.append(segmentationFile)
                        np.save(segmentationFile, predMax)
                    elif mode == MuscleFatSegmentationTask.PROBABILITIES:
                        segmentationFile = os.path.join(outputFileSetPath, f'{file.name()}.seg.prob.npy')
                        segmentationFiles.append(segmentationFile)
                        np.save(segmentationFile, predSqueeze)

                except pydicom.errors.InvalidDicomError:
                    self.addWarning(f'Skipping non-DICOM: {file.path()}')

                # Update progress for this iteration         
                self.updateProgress(step=step, nrSteps=nrSteps)
                step += 1

        # Build output fileset
        outputFileSet = self.dataManager().createFileSet(fileSetPath=outputFileSetPath)

        # Cache all files in the output fileset because it's very likely we'll be using these
        # files again for further processing and visualization
        for file in outputFileSet.files():
            if file.name().endswith('.seg.npy') or file.name().endswith('.seg.prob.npy'):
                writeToCache(file=file, fileObject=np.load(file.path()))

        self.addInfo('Finished')