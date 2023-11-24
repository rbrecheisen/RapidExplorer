from plugins.views.dicomview.layer import Layer


class DicomImageLayer(Layer):
    def __init__(self) -> None:
        super(DicomImageLayer, self).__init__(name='DICOM Image', index=0, opacity=1.0, visible=True)