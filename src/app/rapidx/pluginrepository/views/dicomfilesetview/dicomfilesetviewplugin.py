from rapidx.app.plugins.viewplugin import ViewPlugin


class DicomFileSetViewPlugin(ViewPlugin):
    def __init__(self, parent=None):
        super(DicomFileSetViewPlugin, self).__init__(parent)

    def name(self) -> str:
        return 'DICOM Image Series View'