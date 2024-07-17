import os
import nibabel as nib
import numpy as np
import torch

from totalsegmentator.python_api import totalsegmentator


DIRCTSCANS = 'D:\\Mosamatic\\AutoSliceSelectionBibiToine\\CTscans'
DIRCTSCANSSEGMENTATIONS = 'D:\\Mosamatic\\AutoSliceSelectionBibiToine\\CTscansSegmentations'
DIRL3S = 'D:\\Mosamatic\\AutoSliceSelectionBibiToine\\L3s'
DEVICE = 'gpu'
FAST = False
SELECTEDVERTEBRALROI = 'vertebrae_L3'
VERTEBRAL_ROIS = [
    'vertebrae_L1', 'vertebrae_L2', 'vertebrae_L3', 'vertebrae_L4', 'vertebrae_L5', 'vertebrae_T1', 'vertebrae_T2', 'vertebrae_T3', 
    'vertebrae_T4', 'vertebrae_T5', 'vertebrae_T6', 'vertebrae_T7', 'vertebrae_T8', 'vertebrae_T9', 'vertebrae_T10', 'vertebrae_T11', 
    'vertebrae_T12'
]

def main():

    # check we have L3 images for each CT scan
    for subject_dir_name in os.listdir(DIRCTSCANS):
        assert subject_dir_name + '.dcm' in os.listdir(DIRL3S), f'could not find subject "{subject_dir_name}"'

    for subject_dir_name in os.listdir(DIRCTSCANS):
        subject_dir_path = os.path.join(DIRCTSCANS, subject_dir_name)
        segmentation_output_dir_path = os.path.join(DIRCTSCANSSEGMENTATIONS, subject_dir_name)
        os.makedirs(segmentation_output_dir_path, exist_ok=True)
        assert torch.cuda.is_available(), 'PyTorch GPU support is not availble'

        # run total segmentator
        # totalsegmentator(subject_dir_path, segmentation_output_dir_path, fast=FAST, device=DEVICE)

        # check existence of vertebral ROIs
        for vertebral_roi in VERTEBRAL_ROIS:
            vertebral_roi_file_path = os.path.join(segmentation_output_dir_path, vertebral_roi + '.nii.gz')
            assert os.path.isfile(vertebral_roi_file_path), f'could not find {vertebral_roi}'

        # calculate size of non-zero vertebral masks, except selected ROI
        nr_pixels_non_zero_vertebral_rois = {}
        for vertebral_roi in VERTEBRAL_ROIS:
            vertebral_roi_file_path = os.path.join(segmentation_output_dir_path, vertebral_roi + '.nii.gz')
            data = nib.load(vertebral_roi_file_path).get_fdata()
            nr_pixels = np.sum(data==1)
            if nr_pixels > 0:
                nr_pixels_non_zero_vertebral_rois[vertebral_roi] = nr_pixels

        # check that our selected vertebra's size falls in range
        assert SELECTEDVERTEBRALROI in nr_pixels_non_zero_vertebral_rois.keys(), f'{SELECTEDVERTEBRALROI} has zero shape'

        # calculate minimum and maximum size, except selected ROI and check size selected ROI is within range
        minimum = 999999
        maximum = 0
        for vertebral_roi in nr_pixels_non_zero_vertebral_rois.keys():
            if vertebral_roi == SELECTEDVERTEBRALROI:
                continue
            if nr_pixels_non_zero_vertebral_rois[vertebral_roi] < minimum:
                minimum = nr_pixels_non_zero_vertebral_rois[vertebral_roi]
            if nr_pixels_non_zero_vertebral_rois[vertebral_roi] > maximum:
                maximum = nr_pixels_non_zero_vertebral_rois[vertebral_roi]
        assert minimum < nr_pixels_non_zero_vertebral_rois[SELECTEDVERTEBRALROI] < maximum, f'selected ROI outside of range'

        # check Z-coordinates are in order

        break



if __name__ == '__main__':
    main()