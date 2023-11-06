from rapidx.app.plugins.viewplugin import ViewPlugin


class DicomFileViewPlugin(ViewPlugin):
    def __init__(self, parent=None):
        super(DicomFileViewPlugin, self).__init__(parent)

    def name(self) -> str:
        return 'DICOM Image View'