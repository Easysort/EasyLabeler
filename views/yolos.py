from PyQt5.QtWidgets import (QGroupBox, QPushButton, QVBoxLayout, QProgressBar, QWidget)

from core.state import State
from utils.classes_yoloworld import YOLO_WORLD_CLASSES
from utils.detection import Detection, Bbox
from Easysort.easysort.sorting.infer_yoloWorld import ClassifierYoloWorld
from Easysort.easysort.sorting.infer_yolov8_ultralytics import Classifier

class YoloWidget(QGroupBox):
    def __init__(self, central_widget: QWidget, state: State):
        super().__init__("Auto Detect")
        self.central_widget = central_widget
        self.state = state
        self.classifier = None
        self.yolo_world_classifier = None

        layout = QVBoxLayout()

        self.interpolate_button = QPushButton("Interpolate (the last added bounding box)")
        self.interpolate_button.clicked.connect(lambda: print("Interpolate"))
        # self.interpolate_button.clicked.connect(self.on_interpolate_clicked)
        layout.addWidget(self.interpolate_button)

        self.cancel_interpolate_button = QPushButton("Cancel Interpolation")
        self.cancel_interpolate_button.clicked.connect(lambda: print("Cancel Interpolation"))
        # self.cancel_interpolate_button.clicked.connect(self.on_cancel_interpolate_clicked)
        self.cancel_interpolate_button.setVisible(False)
        layout.addWidget(self.cancel_interpolate_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.run_yolo_detection_button = QPushButton("Run YoloDetection on all frames")
        self.run_yolo_detection_button.clicked.connect(self.on_run_yolo_detection)
        layout.addWidget(self.run_yolo_detection_button)

        self.run_yolo_world_detection_button = QPushButton("Run YoloWorld on all frames")
        self.run_yolo_world_detection_button.clicked.connect(self.on_run_yolo_world_detection)
        layout.addWidget(self.run_yolo_world_detection_button)

        self.setLayout(layout)

    # def on_interpolate_clicked(self):
    #     """Wrapper method to handle interpolate button click"""
    #     self.state.interpolate()

    # def on_cancel_interpolate_clicked(self):
    #     """Wrapper method to handle cancel button click"""
    #     self.state.cancel_interpolation()

    def on_run_yolo_detection(self):
        if self.classifier is None:
            self.classifier = Classifier()

        total_frames = len(self.state.file_names)
        self.progress_bar.setMaximum(total_frames)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        for frame_number, image_path in enumerate(self.state.file_names):
            detections = self.classifier(image_path)
            for yolo_detection in detections:
                # frame, class_id=0, track_id=0, polygon=Polygon(), bbox=Bbox(), keypoints=Keypoints()
                class_id = yolo_detection.boxes.cls.item()
                track_id = self.state.get_next_track_id()
                xywh = yolo_detection.boxes.xywh[0].tolist()
                bbox = Bbox(xywh[0], xywh[1], xywh[2], xywh[3])
                detection = Detection(frame_number, class_id, track_id, bbox=bbox)
                self.state.add_detection(detection)

            self.progress_bar.setValue(frame_number + 1)

        self.progress_bar.setVisible(False)

    def on_run_yolo_world_detection(self):
        if self.yolo_world_classifier is None:
            self.yolo_world_classifier = ClassifierYoloWorld(classes=list(YOLO_WORLD_CLASSES.values()))

        total_frames = len(self.state.file_names)
        self.progress_bar.setMaximum(total_frames)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        for frame_number, image_path in enumerate(self.state.file_names):
            detections = self.yolo_world_classifier(image_path)
            for yolo_detection in detections:
                class_id = yolo_detection[3]
                track_id = self.state.get_next_track_id()
                xywh = yolo_detection[0].tolist()
                bbox = Bbox(xywh[0], xywh[1], xywh[2], xywh[3])
                detection = Detection(frame_number, class_id, track_id, bbox=bbox)
                self.state.add_detection(detection)

            self.progress_bar.setValue(frame_number + 1)

        self.progress_bar.setVisible(False)
