import os
import shutil
import zipfile

# DATADIR = 'D:\\Mosamatic\\T4\\POLYTRAUMA-AnnaVanDijk'
# DATADIROUTPUT = 'D:\\Mosamatic\\T4\\POLYTRAUMA-AnnaVanDijk-Output'
DATADIR = 'D:\\Mosamatic\\T4\\POLYTRAUMA-AnnaVanDijk2\\DataDeel1'
DATADIROUTPUT = 'D:\\Mosamatic\\T4\\POLYTRAUMA-AnnaVanDijk2\\DataOutputDeel1'
os.makedirs(DATADIROUTPUT, exist_ok=False)


def main():
    for f in os.listdir(DATADIR):
        f_path = os.path.join(DATADIR, f)
        patient_name = f.split('_')[0]
        with zipfile.ZipFile(f_path, 'r') as zipref:
            patient_directory = os.path.join(DATADIROUTPUT, patient_name)
            os.makedirs(patient_directory, exist_ok=True)
            zipref.extractall(patient_directory)
            file_path = os.path.join(patient_directory, os.listdir(patient_directory)[0])
            file_path_no_name = os.path.split(file_path)[0]
            shutil.copy(file_path, os.path.join(file_path_no_name, '..', patient_name + '.dcm'))
            print(patient_name)


if __name__ == '__main__':
    main()