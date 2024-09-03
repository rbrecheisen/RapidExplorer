import os
import shutil
import nibabel as nib
import warnings
import torch

from totalsegmentator.python_api import totalsegmentator

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.logger import Logger
from mosamaticdesktop.utils import createNameWithTimestamp
# from mosamaticdesktop.tasks.totalsegmentatortask.checksegmentation import CheckSegmentation
# from mosamaticdesktop.tasks.totalsegmentatortask.sliceselector import SliceSelector
from mosamaticdesktop.tasks.totalsegmentatortask.sliceselector2 import SliceSelector
from mosamaticdesktop.utils import currentTimeInSeconds, elapsedSeconds

warnings.filterwarnings('ignore', 'Invalid value for VR UI')

LOGGER = Logger()

ROIS = [
    'vertebrae_L3',
]


class TotalSegmentatorTask(Task):
    """ This task requires Torch + CUDA. Install using pip:
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    """
    def __init__(self) -> None:
        super(TotalSegmentatorTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Extracts anatomical ROIs from list of full CT scans'
        )
        self.addPathParameter(
            name='rootDirectoryPath',
            labelText='Root Directory of CT Scans (each scan in separate subdirectory)'
        )
        self.addOptionGroupParameter(
            name='vertebra',
            labelText='Select Vertebral Level',
            options=ROIS,
        )
        self.addOptionGroupParameter(
            name='device',
            labelText='Select Device (CPU or GPU)',
            options=['GPU', 'CPU'],
            defaultValue='GPU',
        )
        self.addBooleanParameter(
            name='fast',
            labelText='Enable Fast Calculation (for CPU only)',
            defaultValue=False,
        )
        self.addPathParameter(
            name='outputDirectoryPath',
            labelText='Output Directory'
        )
        self.addTextParameter(
            name='outputDirectoryName',
            labelText='Output Directory Name',
            optional=True,
        )

    def execute(self) -> None:

        # Check we have a GPU available
        if torch.cuda.is_available():

            # Get root directory path containing sub-directories for each CT scan
            rootDirectoryPath = self.parameter('rootDirectoryPath').value()
            if rootDirectoryPath:
                outputDirectoryName = self.parameter('outputDirectoryName').value()
                if outputDirectoryName is None:
                    outputDirectoryName = createNameWithTimestamp(name=outputDirectoryName)
                outputDirectoryPath = self.parameter('outputDirectoryPath').value()
                outputDirectoryPath = os.path.join(outputDirectoryPath, outputDirectoryName)
                os.makedirs(outputDirectoryPath, exist_ok=False)
                LOGGER.info(f'Output directory path: {outputDirectoryPath}')

                # Get vertebra
                vertebra = self.parameter('vertebra').value()
                LOGGER.info(f'vertebra = {vertebra}')

                # Get device and fast options. Disable fast if we're using the GPU
                device = self.parameter('device').value().lower()
                fast = self.parameter('fast').value()
                if device == 'gpu' and fast:
                    fast = False
                LOGGER.info(f'device = {device}, fast = {fast}')

                selectedSlicesDirectoryPath = os.path.join(outputDirectoryPath, 'slices')
                os.makedirs(selectedSlicesDirectoryPath, exist_ok=False)

                # Each CT scan's files should be in a separate subdirectory inside the root directory
                step = 0
                nrSteps = 0
                for scanDirectoryName in os.listdir(rootDirectoryPath):
                    scanDirectoryPath = os.path.join(rootDirectoryPath, scanDirectoryName)
                    if os.path.isdir(scanDirectoryPath):
                        nrSteps += 1

                startTimeTotal = currentTimeInSeconds()
                for scanDirectoryName in os.listdir(rootDirectoryPath):
                    scanDirectoryPath = os.path.join(rootDirectoryPath, scanDirectoryName)
                    if os.path.isdir(scanDirectoryPath):
                        startTime = currentTimeInSeconds()
                        LOGGER.info(f'Running TotalSegmentator on scan directory {scanDirectoryPath}...')
                        outputScanDirectoryPath = os.path.join(outputDirectoryPath, scanDirectoryName)
                        os.makedirs(outputScanDirectoryPath, exist_ok=True)

                        try:
                            # Run Total Segmentator twice, once to get individual NIFTI files for each ROI. 
                            # And once to store all labels in a single NIFTI. This volume will be used for quality checking
                            totalsegmentator(
                                scanDirectoryPath, outputScanDirectoryPath, fast=fast, device=device)
                            roiFilePath = os.path.join(outputScanDirectoryPath, vertebra + '.nii.gz')
                            segmentation = nib.load(roiFilePath)

                            # Get requested ROI and select DICOM slice running through it
                            roi = nib.load(roiFilePath)
                            selector = SliceSelector(roi=roi, volume=segmentation, dicomDirectory=scanDirectoryPath)
                            output_files = selector.execute()
                            if len(output_files) > 0:
                                LOGGER.info(f'Found median slice {output_files[0]} for {vertebra}')
                                selectedSlice = os.path.join(selectedSlicesDirectoryPath, scanDirectoryName + '-' + vertebra + '-' + os.path.split(output_files[0])[1])
                                shutil.copyfile(output_files[0], selectedSlice)
                                LOGGER.info(f'Elapsed time after one scan: {elapsedSeconds(startTime)} seconds')
                            else:
                                LOGGER.error(f'Output of slice selector contains more than one file')
                        except Exception as e:
                            LOGGER.error(f'Exception running Total Segmentator on DICOM files in {scanDirectoryPath} ({e})')

                        self.updateProgress(step=step, nrSteps=nrSteps)
                        step += 1

                self.dataManager().createFileSet(fileSetPath=selectedSlicesDirectoryPath)
                LOGGER.info(f'Total elapsed time: {elapsedSeconds(startTimeTotal)} seconds')
                LOGGER.info('Finished')
                LOGGER.info(f'Results can be found in: {outputDirectoryPath}')
            else:
                LOGGER.error(f'PyTorch: no GPU found. This is going to take forever...')