import os
import shutil
import pydicom
import pydicom.errors
import nibabel as nib
import numpy as np

from typing import List, Dict, Union
from totalsegmentator.python_api import totalsegmentator

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.utils import currentTimeInSeconds, elapsedSeconds
from mosamaticdesktop.logger import Logger

LOGGER = Logger()

ROIS = [
    'vertebrae_S1', 'vertebrae_C1', 'vertebrae_C2', 'vertebrae_C3', 'vertebrae_C4', 'vertebrae_C5', 'vertebrae_C6', 'vertebrae_C7', 
    'vertebrae_L1', 'vertebrae_L2', 'vertebrae_L3', 'vertebrae_L4', 'vertebrae_L5', 'vertebrae_T1', 'vertebrae_T2', 'vertebrae_T3', 
    'vertebrae_T4', 'vertebrae_T5', 'vertebrae_T6', 'vertebrae_T7', 'vertebrae_T8', 'vertebrae_T9', 'vertebrae_T10', 'vertebrae_T11', 
    'vertebrae_T12'
]


class TotalSegmentatorSliceSelectionTask(Task):
    def __init__(self) -> None:
        super(TotalSegmentatorSliceSelectionTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Extracts vertebral images from CT scans'
        )
        self.addPathParameter(
            name='rootDirectoryPath',
            labelText='Root Directory of CT Scans (Each Scan as Separate Sub-Directory)'
        )
        self.addOptionGroupParameter(
            name='vertebra',
            labelText='Vertebral ROI From TotalSegmentator Output',
            options=ROIS,
        )
        self.addPathParameter(
            name='outputDirectoryPath',
            labelText='Output Directory with Selected Images'
        )
        self.addTextParameter(
            name='outputDirectoryName',
            labelText='Output Directory Name',
            optional=True,
        )
        self.addBooleanParameter(
            name='overwriteOutputDirectory',
            labelText='Overwrite Output Directory',
            defaultValue=True,
        )

    def loadNiftiFileAndAffineMatrix(self, path: str) -> Union[np.array, np.array]:
        niftiImage = nib.load(path)
        return niftiImage.get_fdata(), niftiImage.affine

    def calculateBoundingBoxInVoxelSpace(self, maskArray: np.array) -> List[int]:
        if 1 in np.unique(maskArray):
            indices = np.where(maskArray == 1)
            minX, maxX = np.min(indices[0]), np.max(indices[0])
            minY, maxY = np.min(indices[1]), np.max(indices[1])
            minZ, maxZ = np.min(indices[2]), np.max(indices[2])
            boundingBox = (minX, maxX, minY, maxY, minZ, maxZ)
            return boundingBox
        return None

    def calculateBoundingBoxInPatientOrientationSpace(self, boundingBox: List[int], affineMatrix: np.array) -> List[float]:
        min_x, max_x, min_y, max_y, min_z, max_z = boundingBox
        voxelCorners = np.array([
            [min_x, min_y, min_z, 1],
            [min_x, min_y, max_z, 1],
            [min_x, max_y, min_z, 1],
            [min_x, max_y, max_z, 1],
            [max_x, min_y, min_z, 1],
            [max_x, min_y, max_z, 1],
            [max_x, max_y, min_z, 1],
            [max_x, max_y, max_z, 1]
        ])
        transformedCorners = affineMatrix.dot(voxelCorners.T).T
        patientCoordinates = transformedCorners[:, :3]
        min_phys_x, max_phys_x = np.min(patientCoordinates[:, 0]), np.max(patientCoordinates[:, 0])
        min_phys_y, max_phys_y = np.min(patientCoordinates[:, 1]), np.max(patientCoordinates[:, 1])
        min_phys_z, max_phys_z = np.min(patientCoordinates[:, 2]), np.max(patientCoordinates[:, 2])
        boundingBoxInPatientOrientationSpace = (min_phys_x, max_phys_x, min_phys_y, max_phys_y, min_phys_z, max_phys_z)
        return boundingBoxInPatientOrientationSpace

    def calculateBoundingBoxes(self, path: str) -> Dict[str, np.array]:
        boundingBoxes = {}
        for niftiFileName in os.listdir(path):
            roiName = niftiFileName[:-7]
            niftiFilePath = os.path.join(path, niftiFileName)
            maskArray, affineMatrix = self.loadNiftiFileAndAffineMatrix(path=niftiFilePath)
            boundingBoxInVoxelSpace = self.calculateBoundingBoxInVoxelSpace(maskArray=maskArray)
            if boundingBoxInVoxelSpace:
                boundingBoxInPatientOrientationSpace = self.calculateBoundingBoxInPatientOrientationSpace(boundingBox=boundingBoxInVoxelSpace, affineMatrix=affineMatrix)
                self.addInfo(f'{roiName}: {boundingBoxInPatientOrientationSpace}')
                boundingBoxes[roiName] = boundingBoxInPatientOrientationSpace
            else:
                LOGGER.warning(f'{roiName}: empty mask')
        return boundingBoxes

    def execute(self) -> None:

        # Get root directory path containing sub-directories for each CT scan
        rootDirectoryPath = self.parameter('rootDirectoryPath').value()
        if rootDirectoryPath:
            outputDirectoryName = self.parameter('outputDirectoryName').value()
            if outputDirectoryName is None:
                outputDirectoryName = self.generateTimestampForFileSetName(name=outputDirectoryName)
            outputDirectoryPath = self.parameter('outputDirectoryPath').value()
            outputDirectoryPath = os.path.join(outputDirectoryPath, outputDirectoryName)
            self.addInfo(f'Output directory path: {outputDirectoryPath}')

            # Check whether to overwrite previous output directory
            overwriteOutputDirectory = self.parameter('overwriteOutputDirectory').value()
            self.addInfo(f'Overwrite output fileset: {overwriteOutputDirectory}')
            if overwriteOutputDirectory:
                if os.path.isdir(outputDirectoryPath):
                    shutil.rmtree(outputDirectoryPath)
            os.makedirs(outputDirectoryPath, exist_ok=True)

            # Get selected vertebra
            vertebra = self.parameter('vertebra').value()
            if vertebra:

                # Each CT scan's files should be in a separate subdirectory inside the root directory
                step = 0
                nrSteps = 0
                for scanDirectoryName in os.listdir(rootDirectoryPath):
                    scanDirectoryPath = os.path.join(rootDirectoryPath, scanDirectoryName)
                    if os.path.isdir(scanDirectoryPath):
                        nrSteps += 1

                for scanDirectoryName in os.listdir(rootDirectoryPath):
                    scanDirectoryPath = os.path.join(rootDirectoryPath, scanDirectoryName)
                    if os.path.isdir(scanDirectoryPath):

                        # Check if task was canceled first
                        if self.statusIsCanceled():
                            self.addInfo('Canceling task...')
                            break

                        # Store all images in dictionary by Z-coordinate
                        zCoords = {}
                        for fileName in os.listdir(scanDirectoryPath):
                            filePath = os.path.join(scanDirectoryPath, fileName)
                            try:
                                p = pydicom.dcmread(filePath, stop_before_pixels=True)
                                if 'ImagePositionPatient' in p:
                                    zCoords[p.ImagePositionPatient[2]] = filePath
                                else:
                                    self.addError(f'ImagePositionPatient attribute not in DICOM image')
                                    break
                            except pydicom.errors.InvalidDicomError:
                                self.addWarning(f'Image {filePath} of scan {scanDirectoryName} is not valid DICOM. Skipping...')
                                continue

                        self.addInfo(f'Running TotalSegmentator on scan directory {scanDirectoryPath}...')
                        outputScanDirectoryPath = os.path.join(outputDirectoryPath, scanDirectoryName)
                        os.makedirs(outputScanDirectoryPath, exist_ok=True)

                        # # Run TotalSegmentator to extract all vertebrae. We need this in order to check whether
                        # # the vertebra have the correct order and do not overlap
                        # start = currentTimeInSeconds()
                        # totalsegmentator(
                        #     scanDirectoryPath, 
                        #     outputScanDirectoryPath, 
                        #     fast=True,
                        #     roi_subset=ROIS,
                        # )
                        # self.addInfo(f'Elapsed: {elapsedSeconds(start)} seconds')

                        # https://github.com/MaastrichtU-CDS/2022_EvdWouwer_VertebraSegLabel/blob/main/TS_robustness_check.py
                        # Run error checks on extracted vertebrae. Start with the order of their Z-coordinates
                        boundingBoxes = self.calculateBoundingBoxes(path=outputScanDirectoryPath)
                        zMin = float('-inf')
                        for roi in ROIS:
                            if roi in boundingBoxes.keys():
                                boundingBox = boundingBoxes[roi]
                                self.addInfo(f'{roi}: zMin = {boundingBox[4]}')

                        # Select wanted vertebra

                        # Do slice selection on vertebra by taking middle slice
                        
                        # Update progress for this iteration         
                        self.updateProgress(step=step, nrSteps=nrSteps)
                        step += 1

                # Build output fileset

                self.addInfo('Finished processing scan directories')
                self.addInfo(f'Results can be found in: {outputDirectoryPath}')
            else:
                self.addError('No vertebra selected')
        else:
            self.addError('No root directory selected')


