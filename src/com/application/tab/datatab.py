import pydicom
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QAction
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QSlider, QLineEdit, QMenu
from com.application.dataset.dicomseriesloader import DicomSeriesLoader
from com.application.tab import Tab


class DataTab(Tab):

    TITLE = 'Data'
    EMPTY_TEXT = 'No Images Loaded'
    MENU_ITEM_TEXT1 = 'Load DICOM Image'
    MENU_ITEM_TEXT2 = 'Load DICOM Image Series'
    MENU_ITEM_TEXT3 = 'Load Multiple DICOM Image Series'
    DEFAULT_WINDOW_LEVEL = 400
    DEFAULT_WINDOW_WIDTH = 50

    def __init__(self) -> None:
        super(DataTab, self).__init__()
        self._menu = None
        self._imageContent = None
        self._sliderWindowLevelAndWidth = None
        self._lineEditWindowLevelAndWidth = None
        self._selectedDicomSeries = None
        self._windowLevel = DataTab.DEFAULT_WINDOW_LEVEL
        self._windowWidth = DataTab.DEFAULT_WINDOW_WIDTH
        self._initUi()

    def _initUi(self) -> None:
        self._menu = QMenu(DataTab.TITLE)
        # TODO: Create separate actions and connect event handlers
        self._menu.addAction(QAction(DataTab.MENU_ITEM_TEXT1, self))
        self._menu.addAction(QAction(DataTab.MENU_ITEM_TEXT2, self))
        self._menu.addAction(QAction(DataTab.MENU_ITEM_TEXT3, self))
        self._imageContent = QLabel(DataTab.EMPTY_TEXT)
        self._imageContent.setAlignment(Tab.LABEL_ALIGNMENT)
        self._imageContent.setStyleSheet(f'color: {Tab.FONT_COLOR}')
        self._sliderWindowLevelAndWidth = QSlider(Qt.Horizontal)
        self._sliderWindowLevelAndWidth.valueChanged.connect(self._showImage)
        self._sliderWindowLevelAndWidth.setEnabled(False)
        self._lineEditWindowLevelAndWidth = QLineEdit(f'{self._windowLevel}, {self._windowWidth}')
        self._lineEditWindowLevelAndWidth.textChanged.connect(self._updateWindowLevelAndWidth)
        button1 = QPushButton("Load DICOM Image")
        button1.clicked.connect(self._loadDicomImage)
        button2 = QPushButton("Load DICOM Image Series")
        button2.clicked.connect(self._loadDicomImageSeries)
        button3 = QPushButton("Load Multiple DICOM Image Series")
        button3.clicked.connect(self._loadMultipleDicomImageSeries)
        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(self._lineEditWindowLevelAndWidth)
        layout.addWidget(self._imageContent)
        layout.addWidget(self._sliderWindowLevelAndWidth)
        self.setLayout(layout)

    def getMenu(self) -> QMenu:
        return self._menu

    def _loadDicomImage(self) -> None:
        pass

    def _loadDicomImageSeries(self) -> None:
        loader = DicomSeriesLoader(self)
        self._selectedDicomSeries = loader.execute()
        self._sliderWindowLevelAndWidth.setMaximum(len(self._selectedDicomSeries) - 1)
        self._sliderWindowLevelAndWidth.setEnabled(True)
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

    def _showImage(self, idx: int) -> None:
        image = self._selectedDicomSeries[idx].pixel_array
        image = self._applySlopeAndIntercept(self._selectedDicomSeries[idx], image)
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
        # self.window_scale, self.window_width = map(int, self.window_input.text().split(","))
        self._showImage(self._slider.value())
