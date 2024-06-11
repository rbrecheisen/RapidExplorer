import os
import shutil
import warnings
import pydicom

warnings.filterwarnings('ignore', 'Invalid value for VR UI')

ROOTDIR = 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\Data_L3\\Data_manual_L3\\data'
ROOTFULLSCANDIR = 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\Extracted'
ROOTOUTPUTDIR = 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\ExtractedArterialVenousUnenhanced'


def copy_scan_to_output(subject_name, phase_type, series_uid, root_scan_dir):
    target_dir = os.path.join(ROOTOUTPUTDIR, subject_name, phase_type)
    os.makedirs(target_dir, exist_ok=False)
    for d in os.listdir(root_scan_dir):
        if d == subject_name:
            d_path = os.path.join(root_scan_dir, d)
            for f in os.listdir(d_path):
                f_path = os.path.join(d_path, f)
                scan_series_uid = pydicom.dcmread(f_path, stop_before_pixels=True).SeriesInstanceUID
                if scan_series_uid == series_uid:
                    shutil.copy(f_path, os.path.join(target_dir, f))
                    print(f'copied {f_path}')


def main():
    os.makedirs(ROOTOUTPUTDIR, exist_ok=False)
    for phase_type in ['arterial', 'unenhanced', 'venous']:
        phase_dir = os.path.join(ROOTDIR, phase_type, 'raw')
        for f in os.listdir(phase_dir):
            f_path = os.path.join(phase_dir, f)
            subject_name = f.split('_')[0]
            series_uid = pydicom.dcmread(f_path, stop_before_pixels=True).SeriesInstanceUID
            copy_scan_to_output(
                subject_name, phase_type, series_uid, ROOTFULLSCANDIR)


if __name__ == '__main__':
    main()