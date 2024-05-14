"""
There are two options:
(1) Single root directory with subdirectories for each patient where each subdirectory
    contains DIOCM files for multiple scans
(2) Single root directory that contains DICOM files for multiple scans

Parameters:
(1) Root directory: str
(2) Contains subject-specific subdirectories: bool
(3) DICOM attribute(s) to print: List[str]
"""
import os
import shutil
import warnings
import pydicom

warnings.filterwarnings('ignore', 'Invalid value for VR UI')


def get_orientation(orientation):
    if orientation is not None and len(orientation) == 6:
        axial = [1, 0, 0, 0, 1, 0]
        sagittal = [0, 1, 0, 0, 0, -1]
        coronal = [1, 0, 0, 0, 0, -1]
        # Normalize for floating-point imprecisions
        if all(abs(o - a) < 0.1 for o, a in zip(orientation, axial)):
            return 'AXIAL'
        elif all(abs(o - s) < 0.1 for o, s in zip(orientation, sagittal)):
            return 'SAGITTAL'
        elif all(abs(o - c) < 0.1 for o, c in zip(orientation, coronal)):
            return 'CORONAL'
    return 'Orientation is None, not standard or unclear'


def load_dicom_files(root_directory):
    dicom_files = []
    for root, dir, files in os.walk(root_directory):
        for f in files:
            f_path = os.path.join(root, f)
            p = pydicom.dcmread(f_path)
            if 'ImageOrientationPatient' in p:
                orientation = get_orientation(p.ImageOrientationPatient)
                if orientation == 'AXIAL':
                    dicom_files.append((f, p, f_path))
                else:
                    # print(f'Orientation: {orientation}')
                    pass
            else:
                # print(f'Attribute ImageOrientationPatient missing')
                pass
    return dicom_files


def main():
    params = {
        'root_directory': 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\Extracted',
        'output_directory': 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\ExtractedScans',
        'has_suject_subdirectories': False,
    }

    os.makedirs(params['output_directory'], exist_ok=True)

    count = 0
    max_count = -1
    scan_dictionary = {}
    for subject_dir in os.listdir(params['root_directory']):
        subject_dir_path = os.path.join(params['root_directory'], subject_dir)
        if os.path.isdir(subject_dir_path):
            scan_dictionary[subject_dir] = {}
            # Load all DICOM files for this subject
            dicom_files = load_dicom_files(subject_dir_path)
            if len(dicom_files) > 0:
                for dicom_file in dicom_files:
                    series_instance_uid = dicom_file[1].SeriesInstanceUID
                    if series_instance_uid not in scan_dictionary[subject_dir].keys():
                        scan_dictionary[subject_dir][series_instance_uid] = []
                    scan_dictionary[subject_dir][series_instance_uid].append(dicom_file)
                # Copy files to scan directory
                scan_idx = 0
                for series_instance_uid in scan_dictionary[subject_dir].keys():
                    series_output_directory = os.path.join(params['output_directory'], subject_dir, 'scan{:02d}'.format(scan_idx))
                    os.makedirs(series_output_directory, exist_ok=True)
                    for dicom_file in scan_dictionary[subject_dir][series_instance_uid]:
                        shutil.copy(dicom_file[2], os.path.join(series_output_directory, dicom_file[0]))
                    scan_idx += 1
                if count == max_count:
                    break
                count += 1
            else:
                print(f'No DICOM files found for subject {subject_dir}')
        else:
            pass

if __name__ == '__main__':
    main()