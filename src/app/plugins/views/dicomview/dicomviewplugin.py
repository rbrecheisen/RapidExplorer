from plugins.viewplugin import ViewPlugin
from plugins.views.dicomview.dicomview import DicomView

WINDOWCENTER = 50
WINDOWWIDTH = 400
PLUGINNAME = 'DicomViewPlugin'


class DicomViewPlugin(ViewPlugin):
    def __init__(self):
        super(DicomViewPlugin, self).__init__(name=PLUGINNAME, widget=DicomView())
        
    def setData(self, data) -> None:
        self.widget().setData(data)