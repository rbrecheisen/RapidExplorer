import os
import pydicom
import pydicom.errors
import numpy as np

from tasks.taskworkitem import TaskWorkItem
from logger import Logger
from utils import getPixelsFromDicomObject, convertLabelsTo157, normalizeBetween

LOGGER = Logger()


class MuscleFatSegmentationTaskWorkItem(TaskWorkItem):
    def __init__(self) -> None:
        super(MuscleFatSegmentationTaskWorkItem, self).__init__()

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
        try:
            # Read DICOM file and decompress if needed
            p = pydicom.dcmread(file.path())
            p.decompress()

            # Get pixels from DICOM file and normalize to positive range
            img1 = getPixelsFromDicomObject(p, normalize=True)

            # If contour model provided, apply it to detect abdominal contour
            if contourModel:
                self.addInfo('Applying contour model...')
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
                self.addInfo('Generating maximum probability per pixel...')
                predMax = convertLabelsTo157(labelImage=predMax)
                segmentationFile = os.path.join(outputFileSetPath, f'{file.name()}.seg.npy')
                segmentationFiles.append(segmentationFile)
                np.save(segmentationFile, predMax)
            elif self.mode() == 'PROBABILITIES':
                self.addInfo('Generating class probabilities per pixel...')
                segmentationFile = os.path.join(outputFileSetPath, f'{file.name()}.seg.prob.npy')
                segmentationFiles.append(segmentationFile)
                np.save(segmentationFile, predSqueeze)

        except pydicom.errors.InvalidDicomError:
            self.addWarning(f'Skipping non-DICOM: {file.path()}')
