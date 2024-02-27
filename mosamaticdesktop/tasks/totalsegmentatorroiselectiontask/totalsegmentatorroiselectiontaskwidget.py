from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.totalsegmentatorroiselectiontask.totalsegmentatorroiselectiontask import TotalSegmentatorRoiSelectionTask

ROIS = [
    'adrenal_gland_left', 'adrenal_gland_right', 'aorta', 'autochthon_left', 'autochthon_right', 'brain', 'clavicula_left', 
    'clavicula_right', 'colon', 'duodenum', 'esophagus', 'face', 'femur_left', 'femur_right', 'gallbladder', 'gluteus_maximus_left', 
    'gluteus_maximus_right', 'gluteus_medius_left', 'gluteus_medius_right', 'gluteus_minimus_left', 'gluteus_minimus_right', 
    'heart_atrium_left', 'heart_atrium_right', 'heart_myocardium', 'heart_ventricle_left', 'heart_ventricle_right', 'hip_left', 
    'hip_right', 'humerus_left', 'humerus_right', 'iliac_artery_left', 'iliac_artery_right', 'iliac_vena_left', 'iliac_vena_right', 
    'iliopsoas_left', 'iliopsoas_right', 'inferior_vena_cava', 'kidney_left', 'kidney_right', 'liver', 'lung_lower_lobe_left', 
    'lung_lower_lobe_right', 'lung_middle_lobe_right', 'lung_upper_lobe_left', 'lung_upper_lobe_right', 'pancreas', 
    'portal_vein_and_splenic_vein', 'pulmonary_artery', 'rib_left_1', 'rib_left_2', 'rib_left_3', 'rib_left_4', 'rib_left_5', 
    'rib_left_6', 'rib_left_7', 'rib_left_8', 'rib_left_9', 'rib_left_10', 'rib_left_11', 'rib_left_12', 'rib_right_1', 'rib_right_2', 
    'rib_right_3', 'rib_right_4', 'rib_right_5', 'rib_right_6', 'rib_right_7', 'rib_right_8', 'rib_right_9', 'rib_right_10', 'rib_right_11', 
    'rib_right_12', 'sacrum', 'scapula_left', 'scapula_right', 'small_bowel', 'spleen', 'stomach', 'trachea', 'urinary_bladder', 
    'vertebrae_S1', 'vertebrae_C1', 'vertebrae_C2', 'vertebrae_C3', 'vertebrae_C4', 'vertebrae_C5', 'vertebrae_C6', 'vertebrae_C7', 
    'vertebrae_L1', 'vertebrae_L2', 'vertebrae_L3', 'vertebrae_L4', 'vertebrae_L5', 'vertebrae_T1', 'vertebrae_T2', 'vertebrae_T3', 
    'vertebrae_T4', 'vertebrae_T5', 'vertebrae_T6', 'vertebrae_T7', 'vertebrae_T8', 'vertebrae_T9', 'vertebrae_T10', 'vertebrae_T11', 
    'vertebrae_T12', 'heart', 'pulmonary_vein', 'brachiocephalic_trunk', 'subclavian_artery_right', 'subclavian_artery_left', 
    'common_carotid_artery_right', 'common_carotid_artery_left', 'brachiocephalic_vein_left', 'brachiocephalic_vein_right', 
    'atrial_appendage_left', 'superior_vena_cava', 'kidney_cyst_left', 'kidney_cyst_right', 'prostate', 'femur', 'patella', 
    'tibia', 'fibula', 'tarsal', 'metatarsal', 'phalanges_feet', 'humerus', 'ulna', 'radius', 'carpal', 'metacarpal', 'phalanges_hand', 
    'sternum', 'skull', 'subcutaneous_fat', 'skeletal_muscle', 'torso_fat', 'spinal_cord', 'lung_covid_infiltrate', 
    'intracerebral_hemorrhage', 'hip_implant', 'coronary_arteries', 'kidney', 'adrenal_gland', 'thyroid_gland', 'vertebrae_lumbar',
    'vertebrae_thoracic', 'vertebrae_cervical', 'iliac_artery', 'iliac_vena', 'ribs', 'scapula', 'clavicula', 'hip', 'gluteus_maximus', 
    'gluteus_medius', 'gluteus_minimus', 'autochthon', 'iliopsoas', 'lung_vessels', 'lung_trachea_bronchia', 'body_trunc', 
    'body_extremities', 'vertebrae_body', 'lung_pleural', 'pleural_effusion', 'pericardial_effusion', 'liver_vessels', 'liver_tumor', 
    'costal_cartilages'
]


class TotalSegmentatorRoiSelectionTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(TotalSegmentatorRoiSelectionTaskWidget, self).__init__(taskType=TotalSegmentatorRoiSelectionTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass