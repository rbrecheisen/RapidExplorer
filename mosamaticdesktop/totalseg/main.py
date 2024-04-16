import os
import shutil
from starlette.background import BackgroundTasks
from enum import Enum
import threading
import time
import logging
import secrets
import numpy as np
from totalsegmentator.map_to_binary import class_map
from scipy.ndimage import binary_dilation
from skimage.morphology import binary_erosion, ball
from scipy.ndimage import label as label_ndimage
import statistics
import pandas as pd
from collections import Counter

import jwt
import xnat
from barbell2_bodycomp.convert import dcm2nifti
from pydicom import dcmread
from fastapi import FastAPI, Body, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field
from typing import Annotated
import nibabel as nib

logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d :: %(message)s', level = logging.INFO)

# openssl rand -hex 32
JWT_SECRET = '5c31c340b35071a2970f7b9b717c7e3e'
JWT_ALGORITHM = 'HS256'
app = FastAPI()

def update_cache():
    while True:
        if not(os.path.exists(".cache")):
            print("Creating .cache file")
            with open(".cache", "w") as f:
                secret = secrets.token_hex(8)
                f.write(secret)
                print("Secret: {} 1".format(secret))
                f.write(" ")
                f.write("1")
            continue
        with open(".cache", "r+") as f:
            data = f.read().split(" ")
        if time.time() - float(data[1]) > 60*60*24*10:             # 10 days
            with open(".cache", "w") as f:
                secret = secrets.token_hex(8)
                f.write(secret)
                f.write(" ")
                time_now = time.time()
                f.write(str(time_now))
                print("Secret: {} {}".format(secret, time_now))
        time.sleep(60*60*24)

update_cache_thread = threading.Thread(name="update_cache", target=update_cache)
update_cache_thread.start()

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    permission_key = fields.CharField(128)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

class Vertebrae(str, Enum):
    S1 = "S1"
    L5 = "L5"
    L4 = "L4"
    L3 = "L3"
    L2 = "L2"
    L1 = "L1"
    T12 = "T12"
    T11 = "T11"
    T10 = "T10"
    T9 = "T9"
    T8 = "T8"
    T7 = "T7"
    T6 = "T6"
    T5 = "T5"
    T4 = "T4"
    T3 = "T3"
    T2 = "T2"
    T1 = "T1"
    C7 = "C7"
    C6 = "C6"
    C5 = "C5"
    C4 = "C4"
    C3 = "C3"
    C2 = "C2"
    C1 = "C1"

class RequestBody(BaseModel):
    project_name: str
    xnat_url: str
    xnat_username: str
    xnat_password: str
    vertebra: Vertebrae

User_Pydantic = pydantic_model_creator(User, name="User")
# RequestBody_Pydantic = pydantic_model_creator(RequestBody, name="RequestBody")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class MicroManager:
    def __init__(self):
        self.UPLOAD_DIR = "temp"
        if not(os.path.exists(self.UPLOAD_DIR)):
            os.mkdir(self.UPLOAD_DIR)
        self.SLICES_DIR = os.path.join(self.UPLOAD_DIR, "slices")
        self.NIFTI_DIR = os.path.join(self.UPLOAD_DIR, "nifti")
        if not(os.path.exists(self.NIFTI_DIR)):
            os.mkdir(self.NIFTI_DIR)
        self.TS_DIR = os.path.join(self.UPLOAD_DIR, "TS_outputs")
        if not(os.path.exists(self.TS_DIR)):
            os.mkdir(self.TS_DIR)
        self.PROJECT_DIR = "/Users/abhimanyu/Maastricht/Internship/XNAT-TS-Mosamatic-Microservice"

        self.session = None
        self.xnat_project_name = None
        self.thread_complete = True
        self.error_subjects = {}
        self.data_downloaded = True
        self.converted_first_dicom = False

    def cleanup(self):
        shutil.rmtree(self.UPLOAD_DIR)
        os.mkdir(self.UPLOAD_DIR)

    def TotalSegmentator(self, input_file: str, output_path: str, subject: str):
        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path, exist_ok=True)
            cmd = f'TotalSegmentator -i {input_file} -o {output_path} --fast'
            logging.info("TS cmd: {}".format(cmd))
            os.system(cmd)
            output_path = os.path.join(output_path, subject)
            cmd = f'TotalSegmentator -i {input_file} -o {output_path} --ml --fast'
            logging.info("TS cmd: {}".format(cmd))
            os.system(cmd)
            return 200, "Success"
        except Exception as e:
            logging.error("Error: {}".format(e))
            return 501, f"Error in microManager::TotalSegmentator: {e}"

    def sliceSelector(self, subject, TS_path, vertebra: Vertebrae = Vertebrae.L3):
        try:
            FILENAME = "vertebrae_" + vertebra + ".nii.gz"
            PATH = os.path.join(TS_path, FILENAME)
            if not(os.path.exists(self.SLICES_DIR)):
                os.mkdir(self.SLICES_DIR)
            filename = f"{subject}_vertebrae_{vertebra.value}.nii.gz"
            shutil.copyfile(PATH, os.path.join(self.SLICES_DIR, filename))
            return 200, "Success"
        except Exception as e:
            logging.error("Error: {}".format(e))
            return 502, f"Error in sliceSelector: {e}"

    def deleteTheRest(self, TS_path):
        try:
            shutil.rmtree(TS_path)
            return 200, "Success"
        except Exception as e:
            logging.error("Error: {}".format(e))
            return 503, f"Error in microManager::deleteTheRest: {e}"

    def check_segmentation(self, SEG_PATH):
        nii_file = nib.load(SEG_PATH)
        seg = nii_file.get_fdata().astype(int)
        self.check_orientation(seg)
        seg = self.check_vertebrae_masks_consistency(seg)
        self.save_vertebrae_bounding_boxes(seg)
        return 200, "Success"

    def check_vertebrae_masks_consistency(self, seg, radius=2.5):
        try:
            logging.info("----------------------------------------------------------------")
            logging.info(" ---------------------- MASK CHECK -----------------------------")
            logging.info("----------------------------------------------------------------")

            classes_dic = class_map['total']
            logging.info("classes_dic: {}".format(classes_dic))

            # Apply morphological operations to the mask
            # This is done to seperate the segmentation masks of each vertebrae
            struct_elem = ball(radius)  # choose appropriate size and shape of structuring element

            new_seg = np.zeros_like(seg)

            spine = {}

            logging.info("Applying morphological transformations...")

            for label_value in range(18, 42):
                # Create a binary array for the current label value
                # Morphological operations are applied one label at a time
                binary_array = (seg == label_value)
                if np.sum(binary_array) > 0:
                    spine[label_value] = np.sum(binary_array)
                else:
                    continue
                # Apply erosion to the segmentation array
                eroded_array = binary_erosion(binary_array, struct_elem)
                # Apply dilation to the eroded segmentation array
                dilated_array = binary_dilation(eroded_array, struct_elem)
                # Create a binary mask of the dilated segmentation array
                new_seg[dilated_array] = label_value

            logging.info("Separating each 3D mask...")

            # We only keep the labels of the vertebrae
            mask = np.logical_or(seg < 18, seg > 41)
            new_seg[mask] = seg[mask]
            s = new_seg
            # print("mask", mask.shape)
            # print("seg", seg.shape)
            # print("seg[mask]", seg[mask].shape)
            # print("new_seg[mask]", new_seg[mask].shape)
            # with open('seg.npy', 'wb') as f:
            #     np.save(f, seg)
            # with open('new_seg.npy', 'wb') as f:
            #     np.save(f, new_seg)

            # We compute the average size of a vertebra mask
            # This is to distinguish between masks of full vertebrae or "isolated islands"
            # We trim some values to not include the extremes in the average
            # calculate the number of values to trim from both ends

            trim_percentage = 0.1 # define the percentage of values to trim
            trim_count = round(len(spine) * trim_percentage)
            # print("len(spine)", len(spine))
            if trim_count < 1: # trim at least the min and max val
                trim_count = 1
            # print("trim_count", trim_count)
            # sort the values
            sorted_values = sorted(spine.values())
            # print("sorted_values", sorted_values)
            # trim the values
            trimmed_values = sorted_values[trim_count:len(sorted_values) - trim_count]
            # calculate the mean of the trimmed values
            if trimmed_values:
                trimmed_mean = statistics.mean(trimmed_values)
            else:
                trimmed_mean = 0
            # print("trimmed_mean", trimmed_mean)

            mask_arr = np.logical_and(s >= 18, s <= 41)

            # Perform connected component analysis on the mask
            labels, num_labels = label_ndimage(mask_arr)
            # print("num_labels", num_labels)
            # print("labels", labels.shape)

            label_assigned = {}

            logging.info('Checking for inconsistencies in labeling ...')

            # Check each identified 3D mask
            for i in range(1, num_labels + 1):
                mask = (labels == i)
                indices = np.argwhere(mask)
                center = np.mean(indices, axis=0)
                vertebra_labels = s[mask]
                # Count each unique label in the 3D label
                label_counts = Counter(vertebra_labels)
                if len(label_counts) > 1:
                    # Mask contains pixels from multiple vertebrae labels, keep only the largest connected component for the correct label
                    correct_label = max(label_counts, key=label_counts.get)
                    logging.info("Multiple labels are assigned to the same segmentation mask as {}".format(str(classes_dic[correct_label])))
                else:
                    correct_label = list(label_counts.keys())[0]
                # if the label has been previously assigned, we detect what the most plausible error is
                if correct_label in label_assigned:
                    if label_counts[correct_label] < trimmed_mean / 4:
                        logging.info("{} appear more than once. A small seperate section is given this label.".format(str(classes_dic[correct_label])))
                    else:
                        if center[0] < label_assigned[correct_label]:
                            if correct_label < 18:
                                logging.info("{} appear more than once. It might have needed to be assigned the saccrum label.".format(str(classes_dic[correct_label])))
                            else:
                                logging.info("{} appear more than once. It might have needed to be assigned the previous vertebra label.".format(str(classes_dic[correct_label])))
                        else:
                            logging.info("{} appear more than once. It might have needed to be assigned the following vertebra label.".format(str(classes_dic[correct_label])))
                else:
                    # Add the current label to the list of assigned labels
                    label_assigned[correct_label] = center[0]
                logging.info("Check Done")
            return new_seg
        except Exception as e:
            logging.error("Error: {}".format(e))
            return seg

    # Function to save the coordinates of each vertebrae labeled by Total segmentator and ensure the results are consistent
    # Input: seg - the label array of TotalSegmentator
    # Output: None (saves a csv)
    def save_vertebrae_bounding_boxes(self, seg):
        # internal function to define the borders of the bounding box
        def calculate_bounding_box(label):
            indices = np.argwhere(label != 0)
            if len(indices) == 0:
                return None

            min_coords = min(indices, key=lambda sublist: sublist[2])
            max_coords =  max(indices, key=lambda sublist: sublist[2])
            center_coords = (min_coords + max_coords) // 2
            volume = np.count_nonzero(label)

            return {
                "min_coords [z x y]": min_coords,
                "max_coords [z x y]": max_coords,
                "center_coords [z x y]": center_coords,
                "volume": volume
            }
        # iterate through the vertebrae to extract coordinates and check correct order
        labeled_vertebrae = []
        for label in range(18, 42):
            vertebra_label = (seg == label)
            if np.any(vertebra_label):
                bounding_box_info = calculate_bounding_box(vertebra_label)
                if bounding_box_info is not None:
                    if len(labeled_vertebrae) > 0:
                        if label != labeled_vertebrae[-1]["label"] + 1:
                            logging.info("A vertebra label is missing: {}".format(str(labeled_vertebrae[-1]["label"] + 1)))
                            # print("label: " + str(label))
                            # print("labeled_vertebrae[-1][\"label\"] + 1: " + str(labeled_vertebrae[-1]["label"] + 1))
                    labeled_vertebrae.append({
                        "label": label,
                        **bounding_box_info
                    })

        logging.info("{} vertebrae are labeled on this CT image".format(str(len(labeled_vertebrae))))

        df = pd.DataFrame(labeled_vertebrae)
        df.to_csv("vertebrae_info.csv", index=False)

        for index, row in df.iterrows():
            if index > 0:
                if row["center_coords [z x y]"][2] < prev:
                    logging.info("{} doesnt appear in correct position".format(str(row["label"])))
            prev = row["center_coords [z x y]"][2]

    # Function that checks the output of Total segmentator to ensure it wasn't given an image upside down
    # Input: seg - the label array of TotalSegmentator, precision - how many slice tolerance to check order of labels
    # Output: None (prints results on terminal)
    def check_orientation(self, seg, precision=5):
        logging.info("----------------------------------------------------------------")
        logging.info(" ---------------- ORIENTATION CHECK ----------------------------")
        logging.info("----------------------------------------------------------------")

        wrong_orientation = False

        # Each organ and bones is assigned a level to be able to check wheter the segmentation appear in the correct order
        map_organs_to_level = {'brain': 1, 'heart_myocardium': 2, 'heart_atrium_left': 2, 'heart_atrium_right': 2,
                            'heart_ventricle_left': 2
            , 'heart_ventricle_right': 2, 'stomach': 3, 'urinary_bladder': 4}
        map_bones_to_lvl = {'vertebrae_C2': 2, 'vertebrae_C4': 4, 'vertebrae_C6': 6, 'vertebrae_T1': 8, 'vertebrae_T3': 10
            , 'vertebrae_T5': 12, 'vertebrae_T7': 14, 'vertebrae_T9': 16, 'vertebrae_T11': 18, 'vertebrae_L1': 20,
                            'vertebrae_L3': 22
            , 'vertebrae_L5': 24, 'hip_right': 24, 'hip_left': 24, 'sacrum': 24}

        logging.info("Iterating through slices ...")

        classes_dic = class_map["total"]
        # First we loop through the scan to check the organs are correct then we check the bones
        for i in range(2):
            if i == 0:
                map_classes_to_lvl = map_organs_to_level
            if i == 1:
                map_classes_to_lvl = map_bones_to_lvl
            start_index = len(seg[0][0])
            # print("start_index", start_index)
            # print("seg", seg.shape)
            map_lvl_to_classes = {}
            for k, v in map_classes_to_lvl.items():
                map_lvl_to_classes[v] = map_lvl_to_classes.get(v, []) + [k]
            # We loop every 5 slice, for each slice we keep in memory the segmentation that is supposed to be at the "highest level"
            length = seg.shape[2]
            for y in range(length):
                if start_index - precision > precision:
                    start_index = start_index - precision
                    # print("start_index", start_index)
                    slice = seg[:, :, start_index]
                    # slice = seg[start_index]
                    # from the slice we store every unique label
                    count = Counter(slice.flatten())
                    slice = set(slice.flatten())
                    # we remove no label ie 0
                    slice.remove(0)
                    arr = []
                    for el in slice:
                        if count[el] > 20:
                            cat = classes_dic[el]
                            arr.append(cat)
                    # we only keep labels that have been predefined a level to check if they appear in the correct order
                    arr = [i for i in arr if i in map_classes_to_lvl]
                    if len(arr) > 0:
                        # we find out of each label which is at max assigned level
                        max_lvl1 = 1
                        for cat in arr:
                            if map_classes_to_lvl[cat] > max_lvl1:
                                max_lvl1 = map_classes_to_lvl[cat]
                        index = start_index
                        # We loop every x (precision) slice appearing after the slice being currently checked. To make sure every segmentation is at a lower or equal level as the max level identified in slice 1
                        for x in range(start_index - precision):
                            # we repeat the same process on the following slices and compare to max_lvl1
                            if index - precision > 0:
                                index = index - precision
                                slice = seg[:, :, index]
                                # slice = seg[index]
                                count = Counter(slice.flatten())
                                slice = set(slice.flatten())
                                slice.remove(0)
                                arr = []
                                for el in slice:
                                    if count[el] > 20:
                                        cat = classes_dic[el]
                                        arr.append(cat)
                                arr = [i for i in arr if i in map_classes_to_lvl]
                                if len(arr) > 0:
                                    max_lvl2 = 1
                                    for cat in arr:
                                        if map_classes_to_lvl[cat] > max_lvl2:
                                            max_lvl2 = map_classes_to_lvl[cat]
                                    # If 1 of the segmentation is at a lower level, we print a warning of this
                                    if max_lvl2 < max_lvl1:
                                        wrong_orientation = True
                                        logging.info("{}".format(map_lvl_to_classes[max_lvl2]))
                                        logging.info('appear after')
                                        logging.info("{}".format(map_lvl_to_classes[max_lvl1]))
                                        logging.info('----')
                                        break
                        if wrong_orientation:
                            break
        if wrong_orientation:
            logging.info("Input CT scan may not be in the correct orientation")

    def manager(self, vertebra):
        try:
            self.data_downloaded, project_dir = self.getFromXNAT()
            logging.info("project_dir: {}".format(project_dir))
            if not self.data_downloaded:
                return

            # dicomToNifti_thread = threading.Thread(name="dicomToNifti", target=self.dicomToNifti, args=(project_dir,))
            # dicomToNifti_thread.start()

            #TODO: Remove this while loop and replace with thread lock variable thingy
            # while True:
            #     if self.converted_first_dicom:
            #         break
            #     time.sleep(2)

            self.thread_complete = False
            for subject in os.listdir(project_dir):
                status = 200
                msg = ""
                try:
                    self.dicomToNifti(os.path.join(project_dir, subject))
                    input_file = os.path.join(self.NIFTI_DIR, subject, f"{subject}.nii.gz")
                    TS_path = os.path.join(self.TS_DIR, f"{subject}")

                    logging.info("input_file: {}".format(input_file))
                    logging.info("TS_path: {}".format(TS_path))

                    status, msg = self.TotalSegmentator(input_file, TS_path, subject)
                    if status == 501:
                        self.error_subjects[subject] = {}
                        self.error_subjects[subject]["status"] = status
                        self.error_subjects[subject]["msg"] = msg
                        continue
                    logging.info("TS done")

                    logging.info("starting seg check")
                    seg_path = os.path.join(TS_path, f"{subject}.nii")
                    logging.info("seg_path: {}".format(seg_path))
                    status, msg = self.check_segmentation(seg_path)
                    if status == 501:
                        self.error_subjects[subject] = {}
                        self.error_subjects[subject]["status"] = status
                        self.error_subjects[subject]["msg"] = msg
                        continue
                    logging.info("checking segmentation done")

                    status, msg = self.sliceSelector(subject, TS_path, vertebra)
                    if status == 501:
                        self.error_subjects[subject] = {}
                        self.error_subjects[subject]["status"] = status
                        self.error_subjects[subject]["msg"] = msg
                    logging.info("slice selection done")

                    status, msg = self.deleteTheRest(TS_path)
                    if status == 501:
                        self.error_subjects[subject] = {}
                        self.error_subjects[subject]["status"] = status
                        self.error_subjects[subject]["msg"] = msg
                        continue
                    logging.info("deleting the rest done")

                except Exception as e:
                    self.error_subjects[subject] = {}
                    self.error_subjects[subject]["status"] = 501
                    self.error_subjects[subject]["msg"] = f"Error in microManager::manager: {e}"
                    continue
            self.thread_complete = True
        except Exception as e:
            logging.error("Error: {}".format(e))
        return

    def checkDataReadiness(self, background_tasks: BackgroundTasks):
        if not self.data_downloaded:
            return Response(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                content="Download from XNAT was unsuccessful. Please try again",
                media_type="application/xml"
            )
        if os.path.exists(self.SLICES_DIR):
            if not self.thread_complete:
                return Response(
                    status_code=status.HTTP_202_ACCEPTED,
                    content="Data is not ready yet.",
                    media_type="application/xml"
                )
            else:
                shutil.make_archive(self.SLICES_DIR, 'zip', self.SLICES_DIR)
                zip_path = os.path.join(self.UPLOAD_DIR, "slices.zip")
                background_tasks.add_task(self.cleanup)
                return FileResponse(
                    path=zip_path,
                    media_type="application/octet-stream",
                    filename="slices.zip",
                    status_code=status.HTTP_200_OK
                )
        else:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="First process the data, then ask for the slices.",
                media_type="application/xml"
            )

    def checkXNAT(self, project_name: str, xnat_url: str, xnat_username: str, xnat_password: str):
        try:
            try:
                self.session = xnat.connect(xnat_url, user=xnat_username, password=xnat_password, default_timeout=30)
            except:
                return Response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content="Invalid credentials. Check the XNAT URL, username and password (Note: You need to be connected to the UM VPN)",
                    media_type="application/xml"
                )
            # session = xnat.connect('http://137.120.191.233', user='abhi', password='welcome2023', default_timeout=30)

            if not project_name in self.session.projects:
                return Response(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content="The project you were looking for was not found in the XNAT library",
                    media_type="application/xml"
                )

            self.xnat_project_name = project_name

            return Response(
                status_code=status.HTTP_200_OK,
                content="XNAT Data validated",
                media_type="application/xml"
            )
        except Exception as e:
            logging.error("Error:{}".format(e))
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=f"Error in microManager::checkXNAT: {e}",
                media_type="application/xml"
            )

    def getFromXNAT(self):
        try:
            project = self.session.projects[self.xnat_project_name]
            project.download_dir(self.UPLOAD_DIR)
            return True, os.path.join(self.UPLOAD_DIR, self.session.projects[self.xnat_project_name].name)
        except:
            return False, ""

    def getDicomFolder(self, dir):
        rootdir = dir
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file.endswith('.dcm'):
                    dcm_filename = os.path.join(subdir, file).split('/')[-1]
                    dcm_folder = os.path.join(subdir, file).replace(dcm_filename, "")
                    return dcm_folder

    def dicomToNifti(self, project_dir: str):
        try:
            # for folder in os.listdir(project_dir):
            #     dcm_folder = self.getDicomFolder(os.path.join(project_dir, folder))
            #     dcm_obj = dcm2nifti.DicomToNifti()
            #     dcm_obj.input_directory = dcm_folder
            #     dcm_obj.output_file = os.path.join(self.NIFTI_DIR, folder, f"{folder}.nii.gz")
            #     dcm_obj.execute()
            #     self.converted_first_dicom = True

            dcm_folder = self.getDicomFolder(project_dir)
            logging.info("project_dir: {}".format(project_dir))
            dcm_obj = dcm2nifti.DicomToNifti()
            dcm_obj.input_directory = dcm_folder
            logging.info("dcm_folder: {}".format(dcm_folder))
            subject = project_dir.split('/')[-1]
            dcm_obj.output_file = os.path.join(self.NIFTI_DIR, subject, f"{subject}.nii.gz")
            logging.info("output_file: {}".format(dcm_obj.output_file))
            dcm_obj.execute()
            self.converted_first_dicom = True
            return True
        except Exception as e:
            logging.error("Error:".format(e))
            return False

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return await User_Pydantic.from_tortoise_orm(user)

@app.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    # open and read .cache file and get the 16 digit key and compare it with the key provided by the user
    with open(".cache", "r") as f:
        permission_key = f.read()
        # the permission key is the first 16 characters of the .cache file
        permission_key = permission_key[:16]
    print("Permission key: {}".format(permission_key))
    print("User permission key: {}".format(user.permission_key))
    if permission_key != user.permission_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid permission key"
        )
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash), permission_key=user.permission_key)
    await user_obj.save()
    print("User saved")
    user_serialized = await User_Pydantic.from_tortoise_orm(user_obj)
    print("User serialized")
    return user_serialized

@app.get('/user/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    username = user.username
    id = user.id
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Username: {username}, ID: {id}",
        media_type="application/xml"
    )

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# Create an API to get an input dicom file from the user and return the output dicom file
# @router.post("/dicom")
# async def dicom(input_dicom: UploadFile = File, current_user: User_Pydantic = Depends(get_current_user)):
#     ds = dcmread(input_dicom.file, force=True)
#     SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, input_dicom.filename)
#     ds.save_as(SAVE_FILE_PATH)
#     return FileResponse(path=SAVE_FILE_PATH, media_type="application/octet-stream", filename=input_dicom.filename)

@app.post("/ProjectName")
async def from_mosamatic (
        background_tasks: BackgroundTasks,
        request: Annotated[RequestBody, Body(embed=True)],
        current_user: User_Pydantic = Depends(get_current_user)
    ):
    global microObject
    microObject = MicroManager()
    response = microObject.checkXNAT(request.project_name, request.xnat_url, request.xnat_username, request.xnat_password)
    if response.status_code != 200:
        return response

    microManager_thread = threading.Thread(name="microManager", target=microObject.manager, args=(request.vertebra,))
    microManager_thread.start()

    return Response(
        status_code=status.HTTP_202_ACCEPTED,
        content="Received the request. Please wait for the results.",
        media_type="application/xml"
    )

@app.post("/isDataReady")
async def is_data_ready (background_tasks: BackgroundTasks, current_user: User_Pydantic = Depends(get_current_user)):
    global microObject
    try:
        response = microObject.checkDataReadiness(background_tasks)
    except Exception as e:
        response = Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Process the data first",
            media_type="application/xml"
        )
    return response

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["main"]},
    generate_schemas=True,
    add_exception_handlers=True
)
