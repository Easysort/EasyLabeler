from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent

class Keybinds:
    def __init__(self, central_widget: QWidget):
        self.central_widget = central_widget
        self.keybinds = {
            Qt.Key_Space: self.central_widget.play,
            Qt.Key_K: self.central_widget.skip1,
            Qt.Key_L: self.central_widget.skip5,
            Qt.Key_J: self.central_widget.skip_back1,
            Qt.Key_H: self.central_widget.skip_back5,
        }

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in self.keybinds:
            self.keybinds[event.key()]()
