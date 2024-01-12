import os
import json
import shutil
import zipfile
import pydicom
import pydicom.errors
import numpy as np

from typing import List, Any

from tasks.task import Task
# from tasks.taskworkitem import TaskWorkItem
# from tasks.musclefatsegmentationtask.musclefatsegmentationtaskworkitem import MuscleFatSegmentationTaskWorkItem
# from data.datamanager import DataManager
from data.file import File
from configuration import Configuration
from logger import Logger
from utils import getPixelsFromDicomObject, convertLabelsTo157, normalizeBetween

LOGGER = Logger()


class MuscleFatSegmentationTask(Task):
    ARGMAX = 0
    PROBABILITIES = 1

    def __init__(self) -> None:
        super(MuscleFatSegmentationTask, self).__init__()        

    def loadModelFiles(self, files: List[File]) -> List[Any]:
        import tensorflow as tf # Only load TensorFlow package here...
        configuration = Configuration()
        tensorFlowModel, tensorFlowContourModel, parameters = None, None, None
        for file in files:
            filePath = file.path()
            if os.path.split(filePath)[1] == 'model.zip':
                tensorFlowModelFileDirectory = configuration.taskConfigSubDirectory(taskname=__class__.__name__, dirName='tensorFlowModelFiles')
                with zipfile.ZipFile(filePath) as zipObj:
                    zipObj.extractall(path=tensorFlowModelFileDirectory)
                tensorFlowModel = tf.keras.models.load_model(tensorFlowModelFileDirectory, compile=False)
            elif os.path.split(filePath)[1] == 'contour_model.zip':
                tensorFlowModelFileDirectory = configuration.taskConfigSubDirectory(taskname=__class__.__name__, dirName='tensorFlowModelFiles')
                with zipfile.ZipFile(filePath) as zipObj:
                    zipObj.extractall(path=tensorFlowModelFileDirectory)
                tensorFlowContourModel = tf.keras.models.load_model(tensorFlowModelFileDirectory, compile=False)
            elif os.path.split(filePath)[1] == 'params.json':
                with open(filePath, 'r') as f:
                    parameters = json.load(f)
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
        if inputFileSet:   
            self.addInfo(f'Input fileset: {inputFileSet.name()}')

            # Get TensorFlow model fileset
            self.addInfo('Loading TensorFlow model fileset...')
            tensorFlowModelFileSetName = self.parameter('tensorFlowModelFileSetName').value()
            tensorFlowModelFileSet = self.dataManager().fileSetByName(tensorFlowModelFileSetName)
            if tensorFlowModelFileSet:
                self.addInfo(f'TensorFlow model fileset: {tensorFlowModelFileSet.name()}')

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
                os.makedirs(outputFileSetPath, exist_ok=False)
                self.addInfo(f'Output fileset path: {outputFileSetPath}')

                # Get mode (ARGMAX or PROBABILITIES)
                mode = self.parameter('mode').value()
                modeText = 'ARGMAX' if mode == MuscleFatSegmentationTask.ARGMAX else 'PROBABILITIES'
                self.addInfo(f'Mode: {modeText}')

                # Load TensorFlow model files
                model, contourModel, parameters = self.loadModelFiles(files=tensorFlowModelFileSet.files())
                if model and parameters:

                    # Start iterating of the files
                    step = 0
                    files = inputFileSet.files()
                    segmentationFiles = []
                    nrSteps = len(files) + 1
                    for file in files:

                        # Check if task was canceled first
                        if self.statusIsCanceled():
                            self.addInfo('Canceling task...')
                            break

                        try:
                            # Read DICOM file and decompress if needed
                            p = pydicom.dcmread(file.path())
                            p.decompress()

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
                            pred = model.predict([img2])
                            predSqueeze = np.squeeze(pred)

                            # Generate predicted output. Can be ARGMAX (pixel value with maximum probability) or
                            # PROBABILITIES, i.e, the individual class probabilities (muscle, SAT and VAT) in 
                            # each pixel
                            if mode == 'ARGMAX':
                                predMax = predSqueeze.argmax(axis=-1)
                                predMax = convertLabelsTo157(labelImage=predMax)
                                segmentationFile = os.path.join(outputFileSetPath, f'{file.name()}.seg.npy')
                                segmentationFiles.append(segmentationFile)
                                np.save(segmentationFile, predMax)
                            elif self.mode() == 'PROBABILITIES':
                                segmentationFile = os.path.join(outputFileSetPath, f'{file.name()}.seg.prob.npy')
                                segmentationFiles.append(segmentationFile)
                                np.save(segmentationFile, predSqueeze)

                        except pydicom.errors.InvalidDicomError:
                            self.addWarning(f'Skipping non-DICOM: {file.path()}')

                        # Update progress for this iteration         
                        self.updateProgress(step=step, nrSteps=nrSteps)
                        step += 1

                # Build output fileset
                self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
                
                # Update final progress
                self.updateProgress(step=step, nrSteps=nrSteps)
                self.addInfo('Finished')
            else:
                self.addError(f'TensorFlow model fileset {tensorFlowModelFileSetName} not found')
        else:
            self.addError(f'Input fileset {inputFileSetName} not found')