from typing import List

from widgets.viewers.dicomviewer.dicomfile import DicomFile
from widgets.viewers.dicomviewer.segmentationfile import SegmentationFile
from widgets.viewers.dicomviewer.dicomfilelayer import DicomFileLayer
from widgets.viewers.dicomviewer.dicomattributeslayer import DicomAttributesLayer
from widgets.viewers.dicomviewer.segmentationmasklayer import SegmentationMaskLayer


class DicomViewerImage:
    def __init__(self, dicomFilePath: str, index: int) -> None:
        self._dicomFile = DicomFile(filePath=dicomFilePath)
        self._dicomFileLayer = DicomFileLayer(name='dicomFile', index=index)
        self._dicomFileLayer.setFilePath(filePath=self._dicomFile.filePath())
        self._dicomAttributesLayer = DicomAttributesLayer(name='dicomAttributes', index=index)
        self._dicomAttributesLayer.setFilePath(filePath=self._dicomFile.filePath())
        self._dicomAttributesLayer.setInstanceNumber(instanceNumber=self._dicomFile.data().InstanceNumber)
        self._segmentationFile = None
        self._segmentationMaskLayer = None

    def dicomFile(self) -> DicomFile:
        return self._dicomFile
    
    def dicomFileLayer(self) -> DicomFileLayer:
        return self._dicomFileLayer
    
    def dicomAttributesLayer(self) -> DicomAttributesLayer:
        return self._dicomAttributesLayer
    
    def segmentationFile(self) -> SegmentationFile:
        return self._segmentationFile
    
    def segmentationMaskLayer(self) -> SegmentationMaskLayer:
        return self._segmentationMaskLayer

    def setSegmentationFilePath(self, segmentationFilePath: str) -> None:
        self._segmentationFile = SegmentationFile(filePath=segmentationFilePath)
        self._segmentationMaskLayer = SegmentationMaskLayer(name='segmentationMask', opacity=0.5, index=self._dicomFileLayer.index())
        self._segmentationMaskLayer.setFilePath(filePath=self._segmentationFile.filePath())
        self._dicomAttributesLayer.setSegmentationFilePath(filePath=self._segmentationFile.filePath())

    def setWindowCenterAndWidth(self, windowCenterAndWidth: List[int]) -> None:
        self._dicomFileLayer.setWindowCenterAndWidth(windowCenterAndWidth=windowCenterAndWidth)
