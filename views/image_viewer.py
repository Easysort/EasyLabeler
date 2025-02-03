from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QImage
import cv2
import numpy as np

from state import State

class ImageViewer(QWidget):
    def __init__(self, central_widget: QWidget, state: State):
        super().__init__()
        self._state = state
        self.central_widget = central_widget

        self.fixed_width = 1600
        self.fixed_height = 1200
        self.setFixedSize(self.fixed_width, self.fixed_height)
        
        self.setMouseTracking(True)

        self.img = None
        self.zoom = 1
        self.offset = QPoint(0, 0)
        self.on_current_frame_change()

    def on_video_change(self):
        self.on_current_frame_change()

    def on_current_frame_change(self):
        self.current_frame = self._state.current_frame
        self.current_video = self._state.current_video
        image_file = self._state.file_names[self._state.current_frame]
        self.central_widget.update_frame_number(self._state.current_frame, len(self._state.file_names) - 1)
        self.img = cv2.imread(image_file)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img_scale = float(self.fixed_width) / float(self.img.shape[1])
        M = np.float32([
            [self.zoom * self.img_scale, 0, self.offset.x()],
            [0, self.zoom * self.img_scale, self.offset.y()]
        ])
        self.canvas: np.ndarray = cv2.warpAffine(self.img, M, (self.fixed_width, self.fixed_height))
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.canvas is not None:
            height, width, bpc = self.canvas.shape
            bpl = bpc * width
            img = QImage(self.canvas.data, width, height, bpl, QImage.Format_RGB888)
            qp.drawImage(QPoint(0, 0), img)
        qp.end()