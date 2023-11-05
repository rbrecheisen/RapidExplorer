import sys
import os
import numpy as np
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QImage
from pydicom import dcmread

class DicomViewer(QWidget):
    def __init__(self, dicom_dir):
        super().__init__()
        self.dicom_images = []
        self.current_image_index = 0
        self.initUI()
        self.load_dicom_images(dicom_dir)

    def initUI(self):
        self.setWindowTitle('DICOM Viewer')

        self.graphicsView = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        layout = QVBoxLayout()
        layout.addWidget(self.graphicsView)
        self.setLayout(layout)

    def load_dicom_images(self, dicom_dir):
        self.dicom_images.clear()
        dicom_filenames = sorted(os.listdir(dicom_dir))
        
        for filename in dicom_filenames:
            filepath = os.path.join(dicom_dir, filename)
            if os.path.isfile(filepath):
                ds = dcmread(filepath)
                image = self.dicom_array_to_qimage(ds.pixel_array, ds)
                pixmap = QPixmap.fromImage(image)
                self.dicom_images.append(pixmap)
        
        if self.dicom_images:
            self.display_image(0)
        else:
            print("No DICOM images were loaded.")

    def apply_window_level(self, array, window_center, window_width):
        img_min = window_center - window_width // 2
        img_max = window_center + window_width // 2
        windowed = np.clip(array, img_min, img_max)
        windowed = ((windowed - img_min) / (img_max - img_min)) * 255.0
        return windowed.astype(np.uint8)

    def dicom_array_to_qimage(self, array, dataset):
        if 'RescaleSlope' in dataset and 'RescaleIntercept' in dataset:
            array = array * dataset.RescaleSlope + dataset.RescaleIntercept
        array = self.apply_window_level(array, 50, 400)
        if array.dtype != np.uint8:
            array = np.uint8((array - array.min()) / (array.max() - array.min()) * 255)
        height, width = array.shape
        bytes_per_line = width  # For grayscale image
        return QImage(array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

    def display_image(self, index):
        if self.dicom_images:
            pixmap_item = QGraphicsPixmapItem(self.dicom_images[index])
            self.scene.clear()  # Clear the previous image
            self.scene.addItem(pixmap_item)
            self.current_image_index = index

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0 and self.current_image_index > 0:
            self.current_image_index -= 1
        elif delta < 0 and self.current_image_index < len(self.dicom_images) - 1:
            self.current_image_index += 1
        self.display_image(self.current_image_index)

def main():
    app = QApplication(sys.argv)
    dicom_dir = '/Users/ralph/Desktop/downloads/dataset/scan1'
    viewer = DicomViewer(dicom_dir)
    viewer.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
