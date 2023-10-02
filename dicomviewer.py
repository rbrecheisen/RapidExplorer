import sys
import os
import pydicom
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QSlider, QLineEdit

class SimpleDicomViewer(QWidget):
    def __init__(self):
        super(SimpleDicomViewer, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.image_label = QLabel("Image will be displayed here.")
        load_button = QPushButton("Load CT Scan")
        self.window_input = QLineEdit("400,50")
        self.window_scale = 400
        self.window_width = 50
        layout.addWidget(load_button)
        layout.addWidget(self.window_input)
        layout.addWidget(self.image_label)
        layout.addWidget(self.slider)
        load_button.clicked.connect(self.load_images)
        self.slider.valueChanged.connect(self.show_image)
        self.window_input.textChanged.connect(self.update_windowing)
        self.setLayout(layout)
        self.slider.setEnabled(False)

    def update_windowing(self):
        self.window_scale, self.window_width = map(int, self.window_input.text().split(","))
        self.show_image(self.slider.value())

    def load_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder Containing DICOM Files")
        if folder:
            self.dicom_files = [pydicom.dcmread(os.path.join(folder, f)) for f in os.listdir(folder)]
            for p in self.dicom_files:
                p.decompress('pylibjpeg')
            self.dicom_files.sort(key=lambda x: int(x.InstanceNumber))
            self.slider.setMaximum(len(self.dicom_files) - 1)
            self.slider.setEnabled(True)
            self.show_image(0)

    @staticmethod
    def apply_slope_and_intercept(p, image):
        if 'RescaleSlope' in p and 'RescaleIntercept' in p:
            return image * p.RescaleSlope + p.RescaleIntercept
        return image

    @staticmethod
    def apply_window(pixels, window_scale, window_width):
        result = (pixels - window_width + 0.5 * window_scale)/window_scale
        result[result < 0] = 0
        result[result > 1] = 1
        return result

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        current_value = self.slider.value()
        if delta > 0:
            self.slider.setValue(current_value + 1)
        elif delta < 0:
            self.slider.setValue(current_value - 1)

    def show_image(self, index):
        image = self.dicom_files[index].pixel_array
        image = self.apply_slope_and_intercept(self.dicom_files[index], image)
        image = self.apply_window(image, self.window_scale, self.window_width)
        min_value = np.min(image)
        max_value = np.max(image)
        image = np.clip(image, min_value, max_value)
        min_max_range = max_value - min_value
        if min_max_range > 0:
            image = ((image - min_value) / (max_value - min_value) * 255).astype(np.uint8)
        else:
            image = ((image - min_value) / 1 * 255).astype(np.uint8)
        qt_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = SimpleDicomViewer()
    viewer.setWindowTitle("Simple DICOM Viewer")
    viewer.resize(600, 600)
    viewer.show()
    sys.exit(app.exec())

