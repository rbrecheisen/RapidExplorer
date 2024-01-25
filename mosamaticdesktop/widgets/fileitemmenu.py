import os
import sys
import subprocess

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeView

from mosamaticdesktop.widgets.fileitem import FileItem

PLATFORM = sys.platform


class FileItemMenu(QMenu):
    def __init__(self, treeView: QTreeView, fileItem: FileItem, position: QPoint) -> None:
        super(FileItemMenu, self).__init__()
        self._treeView = treeView
        self._fileItem = fileItem
        self._position = position
        action = self.addAction('Find File in Finder/Explorer')
        action.triggered.connect(self.findFileInFinderOrExplorer)

    def findFileInFinderOrExplorer(self):
        if PLATFORM == 'darwin':
            subprocess.run(['open', '-R', self._fileItem.file().path()])
        elif PLATFORM in ['win32', 'cygwin']:
            subprocess.run(['explorer', '/select,', os.path.normpath(self._fileItem.file().path())])
        else:
            pass

    def show(self):
        self.exec_(self._position)