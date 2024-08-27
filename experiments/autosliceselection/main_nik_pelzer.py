import os
import json
import nibabel as nib
import numpy as np
import pydicom.errors
import torch
import pydicom
import pandas as pd

from totalsegmentator.python_api import totalsegmentator
from scipy.ndimage import label, distance_transform_edt
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage.morphology import ball


DIRCTSCANS = 'D:\\Mosamatic\\Nik Pelzer\\CTscans'
DIRCTSCANSSEGMENTATIONS = 'D:\\Mosamatic\\Nik Pelzer\\CTscansSegmentations'
DIRL3S = 'D:\\Mosamatic\\Nik Pelzer\\L3s'
GROUNDTRUTHCOORDS = 'D:\\Mosamatic\\Nik Pelzer\\Truth_reference_selected_slices.csv'
DEVICE = 'gpu'
FAST = False
SELECTEDVERTEBRALROIS = ['vertebrae_L1', 'vertebrae_L2', 'vertebrae_L3', 'vertebrae_L4', 'vertebrae_L5']
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
        if vertebral_roi_name in SELECTEDVERTEBRALROIS:
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


def calculate_best_slice_idx(vertebral_roi, direction):
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
    # row_sum = np.sum(best_slice_mask, axis=1)
    # col_sum = np.sum(best_slice_mask, axis=0)
    # cross_score = row_sum.max() + col_sum.max()
    return best_slice #, cross_score


def calculate_best_slice_z_coordinate(vertebral_roi, direction):
    L3_mask = vertebral_roi.get_fdata()
    affine = vertebral_roi.affine  # Extract the affine matrix from the NIFTI image
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
    if best_slice is not None:
        # Convert the best slice index to a Z-coordinate using the affine matrix
        voxel_coord = [0, 0, best_slice, 1]  # Assuming 0 for X and Y (can be changed as needed)
        real_world_coord = affine.dot(voxel_coord)
        z_coordinate = real_world_coord[2]  # Extract the Z-coordinate
        return z_coordinate
    else:
        return None


def get_middle_slice_z_coordinate_from_vertebral_roi(vertebral_roi):
    z_coordinate = calculate_best_slice_z_coordinate(vertebral_roi, direction=0)
    return z_coordinate


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


def get_ct_scan_dicom_file_for_middle_vertebral_slice_z_coordinate(ct_scan_dir_path, best_z_coordinate):
    ct_scan_dicom_files = []
    for f in os.listdir(ct_scan_dir_path):
        f_path = os.path.join(ct_scan_dir_path, f)
        try:
            dicom_file = pydicom.dcmread(f_path)
            ct_scan_dicom_files.append(dicom_file)
        except pydicom.errors.InvalidDicomError:
            pass
    ct_scan_dicom_files.sort(key=lambda x: x.SliceLocation)
    closest_dicom_file = min(ct_scan_dicom_files, key=lambda x: abs(x.ImagePositionPatient[2] - best_z_coordinate))
    return closest_dicom_file


def load_ground_truth_data_nik_pelzer():
    results = {}
    df = pd.read_csv(GROUNDTRUTHCOORDS, sep=';', index_col='PatientID')
    for idx, row in df.iterrows():
        patient_name = f'Patient{idx:02}'
        if patient_name not in results.keys():
            results[patient_name] = {}
        if row['Vertebra'] == 'L1M':
            results[patient_name]['vertebrae_L1'] = row['Z']
        if row['Vertebra'] == 'L2M':
            results[patient_name]['vertebrae_L2'] = row['Z']
        if row['Vertebra'] == 'L3M':
            results[patient_name]['vertebrae_L3'] = row['Z']
        if row['Vertebra'] == 'L4M':
            results[patient_name]['vertebrae_L4'] = row['Z']
        if row['Vertebra'] == 'L5M':
            results[patient_name]['vertebrae_L5'] = row['Z']
    return results


def main():
    assert torch.cuda.is_available(), 'PyTorch GPU support is not available'
    results_gt = load_ground_truth_data_nik_pelzer()
    results = {}
    for ct_scan_dir_name in os.listdir(DIRCTSCANS):
        try:

            print(f'##### Processing {ct_scan_dir_name}... ######')
            results[ct_scan_dir_name] = {}
            ct_scan_dir_path = os.path.join(DIRCTSCANS, ct_scan_dir_name)
            segmentation_output_dir_path = os.path.join(DIRCTSCANSSEGMENTATIONS, ct_scan_dir_name)
            os.makedirs(segmentation_output_dir_path, exist_ok=True)

            print(f'{ct_scan_dir_name}: Running Total Segmentator...')
            totalsegmentator(ct_scan_dir_path, segmentation_output_dir_path, fast=FAST, device=DEVICE)

            print(f'{ct_scan_dir_name}: Finding best slices...')            
            non_zero_vertebral_rois = get_non_zero_vertebral_rois(segmentation_output_dir_path)
            for vertebral_roi in non_zero_vertebral_rois:
                vertebral_roi_file_path = vertebral_roi.file_map['image'].filename
                vertebral_roi_name = os.path.split(vertebral_roi_file_path)[1][:-7]
                if vertebral_roi_name in SELECTEDVERTEBRALROIS:
                    # best_slice_index = get_middle_slice_from_vertebral_roi(vertebral_roi)
                    # best_ct_scan_dicom_file = get_ct_scan_dicom_file_for_middle_vertebral_slice(ct_scan_dir_path, best_slice_index)
                    # results[ct_scan_dir_name][vertebral_roi_name] = best_ct_scan_dicom_file.InstanceNumber
                    # print(f'{ct_scan_dir_name}[{vertebral_roi_name}]: best slice = {results[ct_scan_dir_name][vertebral_roi_name]}')
                    best_z_coordinate = get_middle_slice_z_coordinate_from_vertebral_roi(vertebral_roi)
                    best_ct_scan_dicom_file = get_ct_scan_dicom_file_for_middle_vertebral_slice_z_coordinate(ct_scan_dir_path, best_z_coordinate)
                    results[ct_scan_dir_name][vertebral_roi_name] = [
                        best_ct_scan_dicom_file.ImagePositionPatient[2], results_gt[ct_scan_dir_name][vertebral_roi_name]
                    ]
                    print(f'{ct_scan_dir_name}[{vertebral_roi_name}]: best slice Z-coordinate = {results[ct_scan_dir_name][vertebral_roi_name]}')
            # break

        except Exception as e:
            print(f'{ct_scan_dir_name}: exception occurred ({e})')

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)


if __name__ == '__main__':
    main()