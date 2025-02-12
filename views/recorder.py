from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QCamera, QCameraInfo, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
import os
import uuid

from core.state import State

class Recorder(QGroupBox):
    def __init__(self, central_widget: QWidget, state: State):
        super().__init__("Recorder")
        self.central_widget = central_widget
        self.state = state

        self.fps = 24
        self.recording = False
        self.frames_index = 0
        self.frame_dir = None
        layout = QVBoxLayout()

        self.open_recorder_button = QPushButton("Open Camera Recorder")
        self.open_recorder_button.clicked.connect(self.open_recorder_window)
        layout.addWidget(self.open_recorder_button)

        self.setLayout(layout)
        self.recorder_window = None

    def open_recorder_window(self): self.recorder_window = RecorderWindow(self.central_widget, self.state); self.recorder_window.show()

class RecorderWindow(QWidget):
    def __init__(self, central_widget: QWidget, state: State):
        super().__init__()
        self.central_widget = central_widget
        self.state = state
        self.setWindowTitle("Camera Recorder")

        self.fps = 24
        self.recording = False
        self.frames_index = 0
        self.frame_dir = None

        layout = QVBoxLayout()

        self.viewfinder = QCameraViewfinder()
        layout.addWidget(self.viewfinder)

        available_cameras = QCameraInfo.availableCameras()
        if available_cameras:
            self.camera = QCamera(available_cameras[0])
            self.camera.setViewfinder(self.viewfinder)
            self.capture = QCameraImageCapture(self.camera)
            self.capture.setCaptureDestination(QCameraImageCapture.CaptureToFile)
            self.capture.imageSaved.connect(self.image_saved)
            
            self.camera.start()
        else:
            self.camera = None
            error_label = QLabel("No camera available")
            layout.addWidget(error_label)

        button_layout = QHBoxLayout()
        self.record_button = QPushButton("Record")
        self.stop_button = QPushButton("Stop")
        self.quit_button = QPushButton("Quit")
        self.record_button.clicked.connect(lambda: self.record(True))
        self.stop_button.clicked.connect(lambda: self.stop_recording())
        self.quit_button.clicked.connect(lambda: self.close())
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.quit_button)
        layout.addLayout(button_layout)

        self.status_label = QLabel()
        self.status_label.setStyleSheet("QLabel { color: gray; }")
        self.status_label.setText("Not Recording")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.capture_frame)
    
    def quit(self):
        self.close()
        self.state.video_list = self.state.find_videos()
        
    def stop_recording(self):
        self.record(False)
        
    def capture_frame(self):
        if self.camera and self.recording:
            self.capture.capture(os.path.join(self.frame_dir, f"frame_{self.frames_index:04d}.jpg"))

    def image_saved(self, id, filename):
        if self.recording:
            self.frames_index += 1

    def record(self, start):
        if not start and self.recording:
            self.recording = False
            self.frames_index = 0
            self.status_label.setText("Not Recording")
            self.status_label.setStyleSheet("QLabel { color: gray; }")
            self.timer.stop()

        if not self.recording and start:
            self.data_folder = str(uuid.uuid4())
            self.frame_dir = os.path.join("data", "new", self.data_folder)
            if not os.path.exists(self.frame_dir): os.makedirs(self.frame_dir)
            self.recording = True
            self.status_label.setText("Recording")
            self.status_label.setStyleSheet("QLabel { color: red; }")
            self.timer.start(1000//self.fps)

    def closeEvent(self, event):
        if self.camera: self.camera.stop(); self.camera = None
        if hasattr(self, 'capture'): self.capture = None
        self.central_widget.reload_video()
        self.timer.stop()
        super().closeEvent(event)
