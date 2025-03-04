from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtGui import QPainter, QImage, QPen, QColor, QFont
import cv2
import numpy as np

from utils.detection import Detection, Bbox
from core.state import State

class ImageViewer(QWidget):
    def __init__(self, central_widget: QWidget, state: State):
        super().__init__()
        self._state = state
        self.central_widget = central_widget

        screen = QApplication.primaryScreen().geometry()
        self.fixed_width = int(screen.width() * 0.7)
        self.fixed_height = int(self.fixed_width * 0.75)
        self.setFixedSize(self.fixed_width, self.fixed_height)
        self.setMouseTracking(True)

        self.img = None
        self.zoom = 1
        self.offset = QPoint(0, 0)

        self.is_creating_detection = False
        self.start_pos = None
        self.current_pos = None
        self.selected_detection = None
        self.dragging_corner = None
        self.corner_index = None
        self.corner_size = 8
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

    def is_near_corner(self, x, y, detection):
        """Check if the mouse is near any corner of the detection"""
        scale = self.zoom * self.img_scale
        screen_corners = np.array(detection.bbox.corners()) * scale + self.offset.x(), self.offset.y()
        for i, (cx, cy) in enumerate(screen_corners[0]):
            if np.sqrt((x - cx)**2 + (y - cy)**2) < 10: return i
        return None

    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == Qt.LeftButton:
            # If we have a selected detection, check if we're near a corner
            if self.selected_detection:
                corner_index = self.is_near_corner(event.pos().x(), event.pos().y(), self.selected_detection)
                if corner_index is not None:
                    self.dragging_corner = True
                    self.corner_index = corner_index
                    self.current_pos = event.pos()
                    return

            # If close to a detection corner, select it
            for detection in self._state.get_frame_detections(self._state.current_frame):
                if detection.is_near_point(event.pos().x(), event.pos().y(), scale = 1/(self.zoom * self.img_scale)):
                    self.selected_detection = None if self.selected_detection and self.selected_detection == detection else detection
                    self.update()
                    return

            if not self.is_creating_detection:
                self.is_creating_detection = True
                self.selected_detection = None
                self.start_pos = event.pos()
                self.current_pos = event.pos()
            else:
                self.is_creating_detection = False
                self.selected_detection = None
                bbox = self.get_bbox_from_points(self.start_pos, self.current_pos)
                detection = Detection(
                    frame=self._state.current_frame,
                    class_id=0,  # Default class # TODO: Add class selection
                    track_id=self._state.get_next_track_id(),
                    bbox=bbox
                )
                self._state.add_detection(detection)
                self.start_pos = None
                self.current_pos = None
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging_corner:
            self.dragging_corner = False
            self.update()
            if self.selected_detection:
                self._state.update_detection(self.selected_detection)

    def mouseMoveEvent(self, event):
        if self.selected_detection and not self.dragging_corner:
            corner_index = self.is_near_corner(event.pos().x(), event.pos().y(), self.selected_detection)
            if corner_index is not None:
                self.setCursor(Qt.SizeFDiagCursor if corner_index in [0, 3] else Qt.SizeBDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        if self.dragging_corner and self.selected_detection:
            self.current_pos = event.pos()
            scale = 1 / (self.zoom * self.img_scale)
            x = (event.pos().x() - self.offset.x()) * scale
            y = (event.pos().y() - self.offset.y()) * scale

            if self.corner_index == 0:  # Top-left
                self.selected_detection.bbox.set_x1(x)
                self.selected_detection.bbox.set_y1(y)
            elif self.corner_index == 1:  # Top-right
                self.selected_detection.bbox.set_x2(x)
                self.selected_detection.bbox.set_y1(y)
            elif self.corner_index == 2:  # Bottom-left
                self.selected_detection.bbox.set_x1(x)
                self.selected_detection.bbox.set_y2(y)
            elif self.corner_index == 3:  # Bottom-right
                self.selected_detection.bbox.set_x2(x)
                self.selected_detection.bbox.set_y2(y)

            self.update()
        elif self.is_creating_detection:
            self.current_pos = event.pos()
            self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.selected_detection:
                self.selected_detection = None
                self.setCursor(Qt.ArrowCursor)
                self.update()
            elif self.is_creating_detection:
                self.is_creating_detection = False
                self.start_pos = None
                self.current_pos = None
                self.update()
        else:
            self.central_widget.keyPressEvent(event)

    def get_bbox_from_points(self, start, end):
        scale = 1 / (self.zoom * self.img_scale)
        x1 = min(start.x(), end.x()) * scale
        y1 = min(start.y(), end.y()) * scale
        x2 = max(start.x(), end.x()) * scale
        y2 = max(start.y(), end.y()) * scale
        return Bbox(x1, y1, x2-x1, y2-y1)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        if self.canvas is not None:
            height, width, bpc = self.canvas.shape
            bpl = bpc * width
            img = QImage(self.canvas.data, width, height, bpl, QImage.Format_RGB888)
            qp.drawImage(QPoint(0, 0), img)

            for detection in self._state.get_frame_detections(self._state.current_frame):
                scale = self.zoom * self.img_scale
                x, y, w, h = detection.bbox.xywh() * scale
                x += self.offset.x()
                y += self.offset.y()

                detection_color = QColor(*detection.color)

                if self.selected_detection and detection == self.selected_detection:
                    qp.setPen(QPen(detection_color, 3))
                    corners = np.array(detection.bbox.corners()) * scale
                    corners += self.offset.x(), self.offset.y()
                    for cx, cy in corners:
                        qp.fillRect(int(cx - self.corner_size/2), int(cy - self.corner_size/2),
                                    self.corner_size, self.corner_size, detection_color)
                else:
                    qp.setPen(QPen(detection_color, 1))

                qp.drawRect(int(x), int(y), int(w), int(h))

                text = detection.class_name
                qp.setFont(QFont("Arial", 8, QFont.Bold))

                metrics = qp.fontMetrics()
                text_width = metrics.width(text)
                text_height = metrics.height()
                padding = 2

                bg_rect = QRect(int(x), int(y - text_height - padding*2),
                              text_width + padding*2, text_height + padding*2)
                qp.fillRect(bg_rect, QColor(0, 0, 0, 160))

                qp.setPen(Qt.white)
                qp.drawText(int(x + padding), int(y - padding), text)

            if self.is_creating_detection and self.start_pos and self.current_pos:
                qp.setPen(Qt.red)
                x = min(self.start_pos.x(), self.current_pos.x())
                y = min(self.start_pos.y(), self.current_pos.y())
                w = abs(self.current_pos.x() - self.start_pos.x())
                h = abs(self.current_pos.y() - self.start_pos.y())
                qp.drawRect(x, y, w, h)

        qp.end()

    # Keybinds for class handling:
    def move_class_id_up(self):
        self.selected_detection.move_class_id_up() if self.selected_detection else None
        self.update()

    def move_class_id_down(self):
        self.selected_detection.move_class_id_down() if self.selected_detection else None
        self.update()

    def move_class_id_up_fraction(self):
        self.selected_detection.move_class_id_up_fraction() if self.selected_detection else None
        self.update()

    def move_class_id_down_fraction(self):
        self.selected_detection.move_class_id_down_fraction() if self.selected_detection else None
        self.update()
