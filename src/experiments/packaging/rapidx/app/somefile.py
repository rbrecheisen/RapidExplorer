from PySide6.QtGui import QPixmap

class SomeClass:
    def doSomething(self):
        pixmap = QPixmap(':/images/cachexia.jpg')
        print(f'pixmap: {pixmap}')
        return 'Done'