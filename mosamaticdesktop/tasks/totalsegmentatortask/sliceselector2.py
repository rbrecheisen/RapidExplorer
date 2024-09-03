import os
import pydicom
import pydicom.errors
import numpy as np


class SliceSelector:
    def __init__(self, roi, volume, dicomDirectory):
        self._roi = roi
        self._volume = volume
        self._dicomDirectory = dicomDirectory

    def calculate_best_slice_z_coordinate(self, vertebral_roi, direction):
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

    def get_middle_slice_z_coordinate_from_vertebral_roi(self, vertebral_roi):
        z_coordinate = self.calculate_best_slice_z_coordinate(vertebral_roi, direction=0)
        return z_coordinate

    def get_ct_scan_dicom_file_for_middle_vertebral_slice_z_coordinate(self, ct_scan_dir_path, best_z_coordinate):
        ct_scan_dicom_files = []
        for f in os.listdir(ct_scan_dir_path):
            f_path = os.path.join(ct_scan_dir_path, f)
            try:
                dicom_file = pydicom.dcmread(f_path)
                ct_scan_dicom_files.append((dicom_file, f_path))
            except pydicom.errors.InvalidDicomError:
                pass
        ct_scan_dicom_files.sort(key=lambda x: x[0].SliceLocation)
        closest_dicom_file = min(ct_scan_dicom_files, key=lambda x: abs(x[0].ImagePositionPatient[2] - best_z_coordinate))
        return closest_dicom_file[1] # file path

    def execute(self):
        best_z_coordinate = self.get_middle_slice_z_coordinate_from_vertebral_roi(self._roi)
        best_ct_scan_dicom_file = self.get_ct_scan_dicom_file_for_middle_vertebral_slice_z_coordinate(self._dicomDirectory, best_z_coordinate)
        return [best_ct_scan_dicom_file]