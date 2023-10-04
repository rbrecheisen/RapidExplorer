from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit, QLabel, QVBoxLayout, QWidget, QToolBar, QStatusBar

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        # Central Panel
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        image_label = QLabel("Image Viewer Placeholder")
        central_layout.addWidget(image_label)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Dock Widgets
        self.dataset_dock = QDockWidget("Datasets")
        self.tasks_dock = QDockWidget("Tasks")
        self.log_dock = QDockWidget("Log")
        
        self.dataset_dock.setWidget(QTextEdit("Dataset Panel"))
        self.tasks_dock.setWidget(QTextEdit("Task Panel"))
        self.log_dock.setWidget(QTextEdit("Log Panel"))

        # Right-side panel with Datasets and Tasks
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dataset_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.tasks_dock)
        self.splitDockWidget(self.dataset_dock, self.tasks_dock, Qt.Vertical)

        # Dock widget at the bottom for logging information
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)

        # Toolbar
        toolbar = QToolBar()
        action1 = QAction(QIcon(QPixmap("icon1.png")), "Action 1", self)
        action2 = QAction(QIcon(QPixmap("icon2.png")), "Action 2", self)
        toolbar.addAction(action1)
        toolbar.addAction(action2)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Status Bar
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

        self.setWindowTitle("QMainWindow with QDockWidgets")
        self.setGeometry(200, 200, 800, 600)

if __name__ == "__main__":
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec()
