import os
import json
import shutil
import pydicom
import pydicom.errors


def get_subject_and_phase_type(f_path):
    file_name = os.path.split(f_path)[1]
    base_file_name = file_name[:-4]
    subject, phase_type = base_file_name.split('_')[0], base_file_name.split('_')[1]
    return subject, phase_type


def get_series_instance_uid(f_path):
    return str(pydicom.dcmread(f_path, stop_before_pixels=True).SeriesInstanceUID)


def main():

    root_dir = 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\Data_L3\\Data_manual_L3\\data'
    scan_dir = 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\ExtractedSplit'
    output_dir = 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\ExtractedSplitPhases\\'
    os.makedirs(output_dir, exist_ok=False)

    file_info = {}
    for d in os.listdir(root_dir):
        d_path = os.path.join(root_dir, d, 'raw')
        if os.path.isdir(d_path):
            for f in os.listdir(d_path):
                f_path = os.path.join(d_path, f)
                subject, phase_type = get_subject_and_phase_type(f_path)
                if phase_type in ['arterial', 'venous', 'unenhanced']:
                    if subject not in file_info.keys():
                        file_info[subject] = {'arterial': '', 'venous': '', 'unenhanced': ''}
                    file_info[subject][phase_type] = get_series_instance_uid(f_path)

    for scan in os.listdir(scan_dir):
        scan_path = os.path.join(scan_dir, scan)
        first_file_name = os.listdir(scan_path)[0]
        first_file_path = os.path.join(scan_path, first_file_name)
        series_instance_uid = pydicom.dcmread(first_file_path, stop_before_pixels=True).SeriesInstanceUID
        subject = scan.split('-')[0]
        subject_dir = os.path.join(output_dir, subject)
        os.makedirs(subject_dir, exist_ok=True)
        if subject in file_info.keys():
            for phase_type in file_info[subject].keys():
                if series_instance_uid == file_info[subject][phase_type]:
                    phase_type_dir = os.path.join(subject_dir, phase_type)
                    os.makedirs(phase_type_dir, exist_ok=True)
                    for f in os.listdir(scan_path):
                        shutil.copy(os.path.join(scan_path, f), phase_type_dir)
        print(f'Saved scan {scan}')
                

if __name__ == '__main__':
    main()