import os
import pydicom
import pydicom.errors
import numpy as np


class SliceSelector:
    def __init__(self, roi, volume, dicomDirectory):
        self._roi = roi
        self._volume = volume
        self._dicomDirectory = dicomDirectory

    @staticmethod
    def get_min_max_slice_idx(roi):
        roi_data = roi.get_fdata()
        nr_slices = roi_data.shape[2]
        i_min = -1
        for i in range(nr_slices):
            slice = roi_data[:,:,i]
            if 1 in np.unique(slice):
                i_min = i
                break
        i_max = -1
        for i in range(nr_slices):
            slice = roi_data[:,:,nr_slices-i-1]
            if 1 in np.unique(slice):
                i_max = nr_slices - i
                break
        return i_min, i_max

    @staticmethod
    def get_z_coord_patient_position(i, volume):
        M = volume.affine[:3, :3]
        abc = volume.affine[:3, 3]
        return (M.dot([0, 0, i]) + abc)[2]

    def get_min_max_z_coord_patient_position(self, i_min, i_max, volume):
        z_min = self.get_z_coord_patient_position(i_min, volume)
        z_max = self.get_z_coord_patient_position(i_max, volume)
        return z_min, z_max

    @staticmethod
    def get_dicom_z(file_path):
        try:
            p = pydicom.dcmread(file_path, stop_before_pixels=True)            
            return p.ImagePositionPatient[2]
        except pydicom.errors.InvalidDicomError:
            pass
        return None

    def get_dicom_images_between(self, z_min, z_max, dicom_directory):
        z_coords = {}
        for f in os.listdir(dicom_directory):            
            f_path = os.path.join(dicom_directory, f)
            z = self.get_dicom_z(f_path)
            if z:
                z_coords[z] = f_path
        z_min_nearest = min(list(z_coords.keys()), key=lambda x:abs(x - z_min))
        z_max_nearest = min(list(z_coords.keys()), key=lambda x:abs(x - z_max))
        file_paths = []
        for z in z_coords.keys():
            if z_min_nearest <= z <= z_max_nearest:
                file_paths.append(z_coords[z])
        return file_paths

    def execute(self):
        i_min, i_max = self.get_min_max_slice_idx(self._roi)
        z_min, z_max = self.get_min_max_z_coord_patient_position(i_min, i_max, self._volume)
        z_median = z_min + np.abs(z_max - z_min) * 0.50
        output_files = self.get_dicom_images_between(z_median, z_median, self._dicomDirectory)
        return output_files