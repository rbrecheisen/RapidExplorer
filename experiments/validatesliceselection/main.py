import os
import pydicom

SLICEDIRAUTO = 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\ExtractedArterialL3\\slices'
SLICEDIRMANUAL = 'D:\\Mosamatic\\P0030_ARTVEN\\20240513\\Data_L3\\Data_manual_L3\\data\\arterial\\raw'


def main():
    """
    For each automatically selected L3 slice, take the subject name and look up the same file in
    the manually selected list of L3 slices. Then you have:
    - slice_auto
    - slice_manual
    Then you look in the DICOM header for the Z-coordinate of both files and calculate their 
    difference in mm's. Add this difference to a dictionary where key = subject name, and 
    value = delta in mm's.
    Print the dictionary
    """
    deltas = {}
    for f_auto in os.listdir(SLICEDIRAUTO):
        subject = f_auto.split('-')[0]
        f_auto_path = os.path.join(SLICEDIRAUTO, f_auto)
        p_auto = pydicom.dcmread(f_auto_path, stop_before_pixels=True)
        z_auto = p_auto.ImagePositionPatient[2]
        for f_manual in os.listdir(SLICEDIRMANUAL):
            if subject == f_manual.split('_')[0]:
                f_manual_path = os.path.join(SLICEDIRMANUAL, f_manual)
                p_manual = pydicom.dcmread(f_manual_path, stop_before_pixels=True)
                z_manual = p_manual.ImagePositionPatient[2]
                slice_thickness = float(p_manual.SliceThickness)
                deltas[subject] = [abs(z_auto - z_manual), slice_thickness]
    for k, v in deltas.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()