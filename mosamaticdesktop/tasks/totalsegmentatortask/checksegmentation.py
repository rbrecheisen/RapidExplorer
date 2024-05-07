import numpy as np
import statistics

from totalsegmentator.map_to_binary import class_map
from scipy.ndimage import binary_dilation
from skimage.morphology import binary_erosion, ball
from scipy.ndimage import label as label_ndimage
from collections import Counter

from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class CheckSegmentation:
    def __init__(self, segmentation, scanName: str):
        self._segmentation = segmentation.get_fdata().astype(int)
        self._scanName = scanName

    def checkVertebraeMasksConsistency(self, seg, radius=2.5):
        try:
            classes_dic = class_map['total']

            # Apply morphological operations to the mask
            # This is done to seperate the segmentation masks of each vertebrae
            struct_elem = ball(radius)  # choose appropriate size and shape of structuring element

            new_seg = np.zeros_like(seg)

            spine = {}

            LOGGER.info("Applying morphological transformations...")

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

            LOGGER.info("Separating each 3D mask...")

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

            LOGGER.info('Checking for inconsistencies in labeling ...')

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
                    LOGGER.info("Multiple labels are assigned to the same segmentation mask as {}".format(str(classes_dic[correct_label])))
                else:
                    correct_label = list(label_counts.keys())[0]
                # if the label has been previously assigned, we detect what the most plausible error is
                if correct_label in label_assigned:
                    if label_counts[correct_label] < trimmed_mean / 4:
                        LOGGER.info("{} appear more than once. A small seperate section is given this label.".format(str(classes_dic[correct_label])))
                    else:
                        if center[0] < label_assigned[correct_label]:
                            if correct_label < 18:
                                LOGGER.info("{} appear more than once. It might have needed to be assigned the saccrum label.".format(str(classes_dic[correct_label])))
                            else:
                                LOGGER.info("{} appear more than once. It might have needed to be assigned the previous vertebra label.".format(str(classes_dic[correct_label])))
                        else:
                            LOGGER.info("{} appear more than once. It might have needed to be assigned the following vertebra label.".format(str(classes_dic[correct_label])))
                else:
                    # Add the current label to the list of assigned labels
                    label_assigned[correct_label] = center[0]
                LOGGER.info("Check Done")
            return True
        except Exception as e:
            LOGGER.error("Error: {}".format(e))
        return False

    def checkOrientation(self, seg, precision=5):
        wrong_orientation = False

        # Each organ and bones is assigned a level to be able to check wheter the segmentation appear in the correct order
        map_organs_to_level = {'brain': 1, 'heart_myocardium': 2, 'heart_atrium_left': 2, 'heart_atrium_right': 2,
                            'heart_ventricle_left': 2
            , 'heart_ventricle_right': 2, 'stomach': 3, 'urinary_bladder': 4}
        map_bones_to_lvl = {'vertebrae_C2': 2, 'vertebrae_C4': 4, 'vertebrae_C6': 6, 'vertebrae_T1': 8, 'vertebrae_T3': 10
            , 'vertebrae_T5': 12, 'vertebrae_T7': 14, 'vertebrae_T9': 16, 'vertebrae_T11': 18, 'vertebrae_L1': 20,
                            'vertebrae_L3': 22
            , 'vertebrae_L5': 24, 'hip_right': 24, 'hip_left': 24, 'sacrum': 24}

        LOGGER.info("Iterating through slices ...")

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
                                        LOGGER.info("{}".format(map_lvl_to_classes[max_lvl2]))
                                        LOGGER.info('appear after')
                                        LOGGER.info("{}".format(map_lvl_to_classes[max_lvl1]))
                                        LOGGER.info('----')
                                        break
                        if wrong_orientation:
                            break
        if wrong_orientation:
            LOGGER.info("Input CT scan may not be in the correct orientation")
            return False
        return True

    def execute(self):
        if self.checkOrientation(self._segmentation):
            if self.checkVertebraeMasksConsistency(self._segmentation):
                return True
        return False