from plugins.views.dicomview.layer import Layer


class DicomAttributeLayer(Layer):
    def __init__(self) -> None:
        super(DicomAttributeLayer, self).__init__(name='DICOM Info', index=-1, opacity=1.0, visible=True)