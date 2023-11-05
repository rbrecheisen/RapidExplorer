import sys
import os
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from pydicom import dcmread

class DicomViewer(QWidget):
    def __init__(self, dicom_dir):
        super().__init__()
        self.dicom_dir = dicom_dir
        self.dicom_files = []
        self.dicom_images_processed = []
        self.current_image_index = 0
        self.window_center = 50
        self.window_width = 400
        self.initUI()
        self.load_dicom_images(self.dicom_dir)

    def initUI(self):
        self.setWindowTitle('DICOM Viewer')
        self.graphicsView = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        # Window level sliders
        self.windowCenterSlider = QSlider(Qt.Horizontal)
        self.windowCenterSlider.setRange(-1024, 3071)
        self.windowCenterSlider.setValue(self.window_center)
        self.windowCenterSlider.valueChanged.connect(self.update_windowing)

        self.windowWidthSlider = QSlider(Qt.Horizontal)
        self.windowWidthSlider.setRange(1, 4096)
        self.windowWidthSlider.setValue(self.window_width)
        self.windowWidthSlider.valueChanged.connect(self.update_windowing)

        self.centerLabel = QLabel('Center:')
        self.widthLabel = QLabel('Width:')

        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.centerLabel)
        sliderLayout.addWidget(self.windowCenterSlider)
        sliderLayout.addWidget(self.widthLabel)
        sliderLayout.addWidget(self.windowWidthSlider)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(sliderLayout)
        layout.addWidget(self.graphicsView)
        self.setLayout(layout)

    def load_dicom_images(self, dicom_dir):
        self.dicom_files = sorted([
            os.path.join(dicom_dir, f) for f in os.listdir(dicom_dir)
            if os.path.isfile(os.path.join(dicom_dir, f))
        ])
        for filepath in self.dicom_files:
            ds = dcmread(filepath)
            self.dicom_images_processed.append(self.dicom_array_to_qimage(ds.pixel_array, ds))
        self.display_image(self.current_image_index)

    def dicom_array_to_qimage(self, array, dataset):
        if 'RescaleSlope' in dataset and 'RescaleIntercept' in dataset:
            array = array * dataset.RescaleSlope + dataset.RescaleIntercept
        array = self.apply_window_level(array, self.window_center, self.window_width)
        if dataset.pixel_array.dtype != np.uint8:
            array = array.astype(np.uint8)
        height, width = array.shape
        bytes_per_line = width
        return QImage(array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

    def apply_window_level(self, image, center, width):
        img_min = center - width // 2
        img_max = center + width // 2
        windowed_image = np.clip(image, img_min, img_max)
        windowed_image = ((windowed_image - img_min) / (img_max - img_min)) * 255.0
        return windowed_image.astype(np.uint8)

    def display_image(self, index):
        if self.dicom_images_processed:
            image = self.dicom_images_processed[index]
            pixmap = QPixmap.fromImage(image)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.clear()
            self.scene.addItem(pixmap_item)
            self.current_image_index = index

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0 and self.current_image_index > 0:
            self.current_image_index -= 1
        elif delta < 0 and self.current_image_index < len(self.dicom_images_processed) - 1:
            self.current_image_index += 1
        self.display_image(self.current_image_index)

    def update_windowing(self):
        self.window_center = self.windowCenterSlider.value()
        self.window_width = self.windowWidthSlider.value()
        # Re-process all images with new window settings
        self.dicom_images_processed = [
            self.dicom_array_to_qimage(dcmread(f).pixel_array, dcmread(f))
            for f in self.dicom_files
        ]
        self.display_image(self.current_image_index)

def main():
    app = QApplication(sys.argv)
    dicom_dir = '/Users/ralph/Desktop/downloads/dataset/scan1'
    viewer = DicomViewer(dicom_dir)
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
