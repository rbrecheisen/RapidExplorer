from typing import Union
import pydicom
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QAction
from PySide6.QtWidgets import QLabel, QVBoxLayout, QSlider, QLineEdit, QMenu, QFileDialog, QWidget, QHBoxLayout

from com.application.dataset.dicomimageseriesdataset import DicomImageSeriesDataset
from com.application.tab.tab import Tab


class DatasetTab(Tab):

    TITLE = 'Dataset'
    EMPTY_TEXT = 'No Images Loaded'
    MENU_ITEM_LOAD_DICOM = 'Load DICOM Image'
    MENU_ITEM_LOAD_DICOM_SERIES = 'Load DICOM Image Series'
    MENU_ITEM_LOAD_MULTI_DICOM_SERIES = 'Load Multiple DICOM Image Series'
    DEFAULT_WINDOW_LEVEL = 400
    DEFAULT_WINDOW_WIDTH = 50

    def __init__(self) -> None:
        super(DatasetTab, self).__init__()
        self._menu = None
        self._imageContent = None
        self._imageContentContainer = None
        self._sliderSliceSelection = None
        self._lineEditWindowLevelAndWidth = None
        self._selectedDataset = None
        self._windowLevel = DatasetTab.DEFAULT_WINDOW_LEVEL
        self._windowWidth = DatasetTab.DEFAULT_WINDOW_WIDTH
        self._initUi()

    def _initUi(self) -> None:

        action1 = QAction(DatasetTab.MENU_ITEM_LOAD_DICOM, self)
        action1.triggered.connect(self._loadDicomImage)
        action2 = QAction(DatasetTab.MENU_ITEM_LOAD_DICOM_SERIES, self)
        action2.triggered.connect(self._loadDicomImageSeries)
        action3 = QAction(DatasetTab.MENU_ITEM_LOAD_MULTI_DICOM_SERIES, self)
        action3.triggered.connect(self._loadMultipleDicomImageSeries)

        self._menu = QMenu(DatasetTab.TITLE)
        self._menu.addAction(action1)
        self._menu.addAction(action2)
        self._menu.addAction(action3)

        self._imageContent = QLabel(DatasetTab.EMPTY_TEXT)
        self._imageContent.setAlignment(Tab.LABEL_ALIGNMENT)
        self._imageContent.setStyleSheet(f'color: {Tab.FONT_COLOR}')

        containerLayout = QHBoxLayout()
        containerLayout.addWidget(self._imageContent)
        containerLayout.setAlignment(self._imageContent, Qt.AlignCenter)
        self._imageContentContainer = QWidget()
        self._imageContentContainer.setLayout(containerLayout)

        self._sliderSliceSelection = QSlider(Qt.Horizontal)
        self._sliderSliceSelection.valueChanged.connect(self._showImage)
        self._sliderSliceSelection.setEnabled(False)

        self._lineEditWindowLevelAndWidth = QLineEdit(f'{self._windowLevel}, {self._windowWidth}')
        self._lineEditWindowLevelAndWidth.textChanged.connect(self._updateWindowLevelAndWidth)

        layout = QVBoxLayout()
        layout.addWidget(self._lineEditWindowLevelAndWidth)
        layout.addWidget(self._imageContentContainer)
        layout.addWidget(self._sliderSliceSelection)
        layout.setAlignment(self._imageContentContainer, Qt.AlignCenter)
        self.setLayout(layout)

    def getMenu(self) -> QMenu:
        return self._menu

    def _loadDicomImage(self) -> None:
        pass

    def _loadDicomImageSeries(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select DICOM Series")
        if path:
            self._selectedDataset = DicomImageSeriesDataset()
            self._selectedDataset.load(path)
            self._sliderSliceSelection.setMaximum(len(self._selectedDataset.series()) - 1)
            self._sliderSliceSelection.setEnabled(True)
            self._showImage(0)

    def _loadMultipleDicomImageSeries(self) -> None:
        pass

    def _applySlopeAndIntercept(self, p: pydicom.Dataset, image: np.ndarray) -> None:
        if 'RescaleSlope' in p and 'RescaleIntercept' in p:
            return image * p.RescaleSlope + p.RescaleIntercept
        return image
    
    def _applyWindowLevelAndWidth(self, image: np.ndarray, window_level: int, window_width: int) -> np.ndarray:
        result = (image - window_width + 0.5 * window_level)/window_level
        result[result < 0] = 0
        result[result > 1] = 1
        return result
    
    def _showImage(self, index) -> None:
        image = self._selectedDataset.image(index).pixel_array
        image = self._applySlopeAndIntercept(self._selectedDataset.image(index), image)
        image = self._applyWindowLevelAndWidth(image, self._windowLevel, self._windowWidth)
        minValue = np.min(image)
        maxValue = np.max(image)
        image = np.clip(image, minValue, maxValue)
        minMaxRange = maxValue - minValue
        if minMaxRange > 0:
            image = ((image - minValue) / (maxValue - minValue) * 255).astype(np.uint8)
        else:
            image = ((image - minValue) / 1 * 255).astype(np.uint8)
        qtImage = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qtImage)
        self._imageContent.setPixmap(pixmap)
        self._imageContent.setScaledContents(True)

    def _updateWindowLevelAndWidth(self) -> None:
        self.window_scale, self.window_width = map(int, self.window_input.text().split(","))
        self._showImage(self._slider.value())
