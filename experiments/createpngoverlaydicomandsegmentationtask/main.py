import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimage


DICOMIMAGES = ["D:\\Mosamatic\\Karlijn Demers\\11-008_L3_CTabd_18122019.dcm.png", "D:\\Mosamatic\\Karlijn Demers\\14-014_L3_CTabd_23062020.dcm.png"]
SEGMENTATIONIMAGES = ["D:\\Mosamatic\\Karlijn Demers\\11-008_L3_CTabd_18122019.dcm.seg.npy.png", "D:\\Mosamatic\\Karlijn Demers\\14-014_L3_CTabd_23062020.dcm.seg.npy.png"]
OUTPUTIMAGEDIR = 'D:\\Mosamatic\\Karlijn Demers\\OverlayImages'


def main():

    os.makedirs(OUTPUTIMAGEDIR, exist_ok=True)
    
    for i in range(2):

        dicom_image = mpimage.imread(DICOMIMAGES[i])
        segmentation_image = mpimage.imread(SEGMENTATIONIMAGES[i])
        
        black_pixels = (segmentation_image[:, :, 0:3] == 0).all(axis=2)
        segmentation_image[black_pixels, 3] = 0

        alpha = 0.75
        
        fig, ax = plt.subplots()
        ax.imshow(dicom_image, alpha=1)
        ax.imshow(segmentation_image, alpha=alpha)
        ax.axis('off')

        output_image_name = os.path.split(DICOMIMAGES[i])[1] + f'.opacity-{alpha}.png'
        output_image_path = os.path.join(OUTPUTIMAGEDIR, output_image_name)

        plt.savefig(
            output_image_path, 
            bbox_inches='tight', 
            pad_inches=0, 
            transparent=True
        )


if __name__ == '__main__':
    main()