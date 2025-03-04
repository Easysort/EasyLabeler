import unittest
from PyQt5.QtWidgets import QApplication
import sys
import os
from main import CentralWidget
from views.frame_manipulation import FrameManipulationWidget
from pathlib import Path
import shutil
from config import DATA_DIR
from tests.test_utils import get_dummy_detection, UniversalCleanup

class TestFrameManipulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
        cls.central_widget = CentralWidget()
        cls.frame_manipulation_widget = FrameManipulationWidget(cls.central_widget, cls.central_widget.state)
        cls.frame_manipulation_widget.admin_mode.setChecked(True)
        cls.central_widget.state.current_video = "new/test"
        cls.cleanup = UniversalCleanup()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup.cleanup()
        cls.app.quit()

    def copy_video(self) -> tuple[CentralWidget, FrameManipulationWidget]:
        central_widget: CentralWidget = self.central_widget
        frame_manipulation_widget: FrameManipulationWidget = self.frame_manipulation_widget
        frame_manipulation_widget.admin_mode.setChecked(True)
        path = Path("data") / Path("new/test")
        copied_path = Path("data/new/test_temp")
        self.cleanup.add_file(copied_path)
        os.makedirs(copied_path, exist_ok=True)
        shutil.copytree(path, copied_path, dirs_exist_ok=True)
        central_widget.state.set_current_video("new/test_temp")
        central_widget.state.load_videos()
        return central_widget, frame_manipulation_widget

    def test_delete_video(self):
        central_widget, frame_manipulation_widget = self.copy_video()
        copied_path = DATA_DIR / Path("new/test_temp")
        self.assertTrue(central_widget.state.current_video == "new/test_temp")
        self.assertTrue(copied_path.exists())
        frame_manipulation_widget.delete_video()
        self.assertFalse(copied_path.exists())

    def test_delete_frames(self):
        central_widget, frame_manipulation_widget = self.copy_video()
        central_widget.state.change_frame(2)
        assert central_widget.state.current_frame == 2
        assert len(central_widget.state.file_names) == 5
        central_widget.state.reset_annotations()
        assert len(central_widget.state.detections) == 0
        central_widget.state.add_detection(get_dummy_detection(0, track_id=2))
        central_widget.state.add_detection(get_dummy_detection(2))
        central_widget.state.add_detection(get_dummy_detection(4, track_id=1))
        frame_manipulation_widget.delete_previous_frames()
        assert len(central_widget.state.detections) == 2
        assert central_widget.state.detections[0].frame == 0
        assert central_widget.state.current_frame == 0
        assert len(central_widget.state.file_names) == 3
        frame_manipulation_widget.admin_mode.setChecked(True)
        frame_manipulation_widget.delete_future_frames()
        assert central_widget.state.current_frame == 0
        assert len(central_widget.state.file_names) == 1
        assert len(central_widget.state.detections) == 1
        assert central_widget.state.detections[0].frame == 0
        assert len(central_widget.state.detections) == 1, f"Detections: {central_widget.state.detections}"
        copied_path = DATA_DIR / Path("new/test_copy")
        self.assertFalse(copied_path.exists())

if __name__ == "__main__":
    unittest.main()