from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QWidget, QCheckBox
import os
import shutil

from core.state import State
from config import DATA_DIR

class FrameManipulationWidget(QGroupBox):
    def __init__(self, central_widget: QWidget, state: State):
        super().__init__("Frame Manipulation")
        self.central_widget = central_widget
        self.state = state

        layout = QVBoxLayout()

        self.admin_mode = QCheckBox("Admin mode")
        self.delete_video_button = QPushButton("Delete video")
        self.delete_previous_frames_button = QPushButton("Delete all previous frames")
        self.delete_future_frames_button = QPushButton("Delete all future frames")

        self.delete_video_button.clicked.connect(self.delete_video)
        self.delete_previous_frames_button.clicked.connect(self.delete_previous_frames)
        self.delete_future_frames_button.clicked.connect(self.delete_future_frames)

        layout.addWidget(self.admin_mode)
        layout.addWidget(self.delete_video_button)
        layout.addWidget(self.delete_previous_frames_button)
        layout.addWidget(self.delete_future_frames_button)
        self.setLayout(layout)

    def delete_video(self):
        if not self.admin_mode.isChecked(): return
        shutil.rmtree(os.path.join(DATA_DIR, self.state.current_video))

    def delete_previous_frames(self):
        if not self.admin_mode.isChecked(): return
        current_frame = self.state.current_frame
        for frame in self.state.file_names[:current_frame]: os.remove(frame)
        self.state.load_files()
        self.state.current_frame = 0
        for detection in self.state.detections.values(): detection.frame -= current_frame

    def delete_future_frames(self):
        if not self.admin_mode.isChecked(): return
        for frame in self.state.file_names[self.state.current_frame + 1:]:
            os.remove(frame)
        self.state.load_files()
        # TODO: Remove detections for these deleted frames
