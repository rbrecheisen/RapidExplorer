import os
import nibabel as nib
import numpy as np
import pydicom.errors
import torch
import pydicom

from totalsegmentator.python_api import totalsegmentator
from scipy.ndimage import label, distance_transform_edt
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.morphology import ball


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


def load_instance_numbers(L3_dir_path):
    instance_numbers = {}
    for f in os.listdir(L3_dir_path):
        f_path = os.path.join(L3_dir_path, f)
        subject_name = f[:-4] if f.endswith('.dcm') else f
        try:
            p = pydicom.dcmread(f_path, stop_before_pixels=True)
            instance_numbers[subject_name] = p.InstanceNumber
        except pydicom.errors.InvalidDicomError:
            pass
    return instance_numbers


def check_z_coordinates_ct_images_match_nifti_volume(ct_scan_dir_path, nifti_volume_file_path):
    z_min_ct_scan = 999999
    z_max_ct_scan = -z_min_ct_scan
    for f in os.listdir(ct_scan_dir_path):
        f_path = os.path.join(ct_scan_dir_path, f)
        p = pydicom.dcmread(f_path, stop_before_pixels=True)
        z = p.ImagePositionPatient[2]
        if z < z_min_ct_scan:
            z_min_ct_scan = z
        if z > z_max_ct_scan:
            z_max_ct_scan = z
    nifti_volume = nib.load(nifti_volume_file_path)
    nifti_volume_array = nifti_volume.get_fdata()
    nifti_volume_affine = nifti_volume.affine
    z_min_nifti_volume = nifti_volume_affine[2, 3]
    z_max_nifti_volume = nifti_volume_affine[2, 3] + (nifti_volume_array.shape[2] - 1) * nifti_volume_affine[2, 2]
    assert np.isclose(z_min_ct_scan, z_min_nifti_volume) and np.isclose(z_max_ct_scan, z_max_nifti_volume)


def get_non_zero_vertebral_rois(segmentation_output_dir_path):
    non_zero_verterbral_rois = []
    for vertebral_roi in VERTEBRAL_ROIS:
        vertebral_roi_file_path = os.path.join(segmentation_output_dir_path, vertebral_roi + '.nii.gz')
        data = nib.load(vertebral_roi_file_path)
        data_array = data.get_fdata()
        nr_voxels = np.sum(data_array==1)
        if nr_voxels > 0:
            non_zero_verterbral_rois.append(data)
    return non_zero_verterbral_rois


def check_vertebral_rois_exists(segmentation_output_dir_path):
    for vertebral_roi in VERTEBRAL_ROIS:
        vertebral_roi_file_path = os.path.join(segmentation_output_dir_path, vertebral_roi + '.nii.gz')
        assert os.path.isfile(vertebral_roi_file_path), f'could not find {vertebral_roi}'


def check_nr_voxels_selected_roi_within_range(non_zero_vertebral_rois):
    minimum = 999999
    maximum = 0
    for vertebral_roi in non_zero_vertebral_rois:
        vertebral_roi_file_path = vertebral_roi.file_map['image'].filename
        vertebral_roi_name = os.path.split(vertebral_roi_file_path)[1][:-7]
        data = vertebral_roi.get_fdata()
        nr_voxels = np.sum(data==1)
        if vertebral_roi_name == SELECTEDVERTEBRALROI:
            selected_nr_voxels = nr_voxels
            continue
        if nr_voxels < minimum:
            minimum = nr_voxels
        if nr_voxels > maximum:
            maximum = nr_voxels
    assert minimum < selected_nr_voxels < maximum, f'selected ROI outside of range'


def check_z_coordinates_in_order(non_zero_vertebral_rois):
    """
    This method does not work because each vertebra consists of multiple components. We only want the largest component
    which is the bony structure through which the spinal nerves run I think. Perhaps use post-processing to identify the
    separate components, count the number of voxels in each, and take the largest?
    """
    def get_z_min_z_max_for_nifti_volume(nifti_volume_array, affine):
        non_zero_indices = np.argwhere(nifti_volume_array != 0)
        z_coords = non_zero_indices[:, 2]
        first_non_zero_voxel_index = z_coords.min()
        last_non_zero_voxel_index = z_coords.max()
        z_first_non_zero = affine[2, 3] + first_non_zero_voxel_index * affine[2, 2]
        z_last_non_zero = affine[2, 3] + last_non_zero_voxel_index * affine[2, 2]
        return z_first_non_zero, z_last_non_zero
    z_min_last = -999999
    z_max_last = -999999
    for vertebral_roi in non_zero_vertebral_rois:
        print('Checking Z-coordinates {}...'.format(vertebral_roi.file_map['image'].filename))
        vertebral_roi_array = vertebral_roi.get_fdata()
        vertebral_roi_affine = vertebral_roi.affine
        z_min, z_max = get_z_min_z_max_for_nifti_volume(vertebral_roi_array, vertebral_roi_affine)
        print(f'z_min_last: {z_min_last}, z_min: {z_min}, z_max_last: {z_max_last}, z_max: {z_max}')
        assert z_min > z_min_last
        z_min_last = z_min
        assert z_max > z_max_last
        z_max_last = z_max


# def get_largest_component_from_vertebral_roi(vertebral_roi):
#     data = vertebral_roi.get_fdata().astype(np.int32)
#     distance = distance_transform_edt(data)
#     local_maxi = np.zeros_like(data, dtype=bool)
#     local_maxi[tuple(peak_local_max(distance, labels=data, footprint=ball(2)).T)] = True
#     if local_maxi.shape != data.shape:
#         local_maxi = np.reshape(local_maxi, data.shape)
#     assert local_maxi.shape == data.shape, "Shape mismatch between local_maxi and data."
#     markers, _ = label(local_maxi)
#     assert markers.shape == data.shape, "Shape mismatch between markers and data."
#     labels = watershed(-distance, markers, mask=data)
#     sizes = np.bincount(labels.ravel())
#     sizes = sizes[1:]
#     largest_component = np.argmax(sizes) + 1
#     largest_mask = np.where(labels == largest_component, 1, 0)
#     largest_mask_image = nib.Nifti1Image(largest_mask.astype(np.uint8), vertebral_roi.affine)
#     return largest_mask_image


def calculate_best_slice_and_cross_score(vertebral_roi, direction):
    L3_mask = vertebral_roi.get_fdata()
    max_lateral_extent = 0
    best_slice = None
    for i in range(L3_mask.shape[2]):
        slice_mask = L3_mask[:, :, i]
        non_zero_coords = np.where(slice_mask)
        if len(non_zero_coords[direction]) > 0:
            lateral_extent = non_zero_coords[direction].max() - non_zero_coords[direction].min()
            if lateral_extent > max_lateral_extent:
                max_lateral_extent = lateral_extent
                best_slice = i
    best_slice_mask = L3_mask[:, :, best_slice]
    row_sum = np.sum(best_slice_mask, axis=1)
    col_sum = np.sum(best_slice_mask, axis=0)
    cross_score = row_sum.max() + col_sum.max()
    return best_slice, cross_score


def get_middle_slice_from_vertebral_roi(vertebral_roi):
    best_slice = -1
    best_slice_rows, cross_score_rows = calculate_best_slice_and_cross_score(vertebral_roi, direction=0)
    best_slice_cols, cross_score_cols = calculate_best_slice_and_cross_score(vertebral_roi, direction=1)
    if cross_score_rows > cross_score_cols:
        best_slice = best_slice_rows
    else:
        best_slice = best_slice_cols
    return best_slice


def get_ct_scan_dicom_file_for_middle_vertebral_slice(ct_scan_dir_path, best_slice_index):
    ct_scan_dicom_files = []
    for f in os.listdir(ct_scan_dir_path):
        f_path = os.path.join(ct_scan_dir_path, f)
        try:
            ct_scan_dicom_files.append(pydicom.dcmread(f_path))
        except pydicom.errors.InvalidDicomError:
            pass
    ct_scan_dicom_files.sort(key=lambda x: x.SliceLocation)
    return ct_scan_dicom_files[len(ct_scan_dicom_files) - best_slice_index - 1]


def main():
    assert torch.cuda.is_available(), 'PyTorch GPU support is not available'
    instance_numbers = load_instance_numbers(DIRL3S)
    for ct_scan_dir_name in os.listdir(DIRCTSCANS):
        assert ct_scan_dir_name + '.dcm' in os.listdir(DIRL3S), f'could not find subject "{ct_scan_dir_name}"'
    for ct_scan_dir_name in os.listdir(DIRCTSCANS):
        ct_scan_dir_path = os.path.join(DIRCTSCANS, ct_scan_dir_name)
        segmentation_output_dir_path = os.path.join(DIRCTSCANSSEGMENTATIONS, ct_scan_dir_name)
        os.makedirs(segmentation_output_dir_path, exist_ok=True)
        
        # check_z_coordinates_ct_images_match_nifti_volume(ct_scan_dir_path, os.path.join(segmentation_output_dir_path, SELECTEDVERTEBRALROI + '.nii.gz'))
        # check_vertebral_rois_exists(segmentation_output_dir_path)
        # check_nr_voxels_selected_roi_within_range(non_zero_vertebral_rois)
        # check_z_coordinates_in_order(non_zero_vertebral_rois)

        totalsegmentator(ct_scan_dir_path, segmentation_output_dir_path, fast=FAST, device=DEVICE)
        
        non_zero_vertebral_rois = get_non_zero_vertebral_rois(segmentation_output_dir_path)
        for vertebral_roi in non_zero_vertebral_rois:
            vertebral_roi_file_path = vertebral_roi.file_map['image'].filename
            vertebral_roi_name = os.path.split(vertebral_roi_file_path)[1][:-7]
            if vertebral_roi_name == SELECTEDVERTEBRALROI:
                best_slice_index = get_middle_slice_from_vertebral_roi(vertebral_roi)
                best_ct_scan_dicom_file = get_ct_scan_dicom_file_for_middle_vertebral_slice(ct_scan_dir_path, best_slice_index)
                assert instance_numbers[ct_scan_dir_name] - 1 <= best_ct_scan_dicom_file.InstanceNumber <= instance_numbers[ct_scan_dir_name] + 1
                print(f'{ct_scan_dir_name}: Instance number = {best_ct_scan_dicom_file.InstanceNumber}')
                break


if __name__ == '__main__':
    main()