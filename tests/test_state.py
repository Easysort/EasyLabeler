import unittest
from PyQt5.QtWidgets import QApplication
import sys
from main import CentralWidget
from utils.detection import Detection
from core.state import State

class TestState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
        cls.central_widget = CentralWidget()
        cls.state: State = cls.central_widget.state
        cls.state.current_video = "new/test"

    @classmethod
    def tearDownClass(cls):
        # Add universal cleanup
        cls.app.quit()

    def setUp(self):
        self.state.reset_annotations()

    def test_init_state(self):
        self.state.load_annotations()
        self.assertEqual(len(self.state.detections), 2)
        self.state.reset_annotations()
        self.assertEqual(len(self.state.detections), 0)

    def test_add_detection(self):
        self.assertEqual(len(self.state.detections), 0)
        self.state.add_detection(Detection(frame=0, class_id=0, track_id=0, bbox=[0, 0, 100, 100]))
        self.assertEqual(len(self.state.detections), 1)

    def test_delete_detection(self):
        self.state.add_detection(Detection(frame=0, class_id=0, track_id=4, bbox=[0, 0, 100, 100]))
        self.assertEqual(len(self.state.detections), 1)
        self.state.delete_detection([4])
        self.assertEqual(len(self.state.detections), 0)

    def test_update_detection(self):
        self.state.add_detection(Detection(frame=0, class_id=0, track_id=4, bbox=[0, 0, 100, 100]))
        self.assertEqual(len(self.state.detections), 1)
        print(self.state.detections)
        self.state.update_detection(Detection(frame=0, class_id=0, track_id=4, bbox=[0, 0, 200, 200]))
        self.assertEqual(len(self.state.detections), 1)
        print(self.state.detections)
        self.assertEqual(self.state.detections[4].bbox.xywh().tolist(), [0, 0, 200, 200])

    def test_asserts(self):
        self.state.add_detection(Detection(frame=0, class_id=0, track_id=4, bbox=[0, 0, 100, 100]))
        with self.assertRaises(AssertionError):
            self.state.add_detection(Detection(frame=0, class_id=0, track_id=4, bbox=[0, 0, 100, 100]))
        with self.assertRaises(AssertionError):
            self.state.update_detection(Detection(frame=0, class_id=0, track_id=5, bbox=[0, 0, 100, 100]))
        with self.assertRaises(AssertionError):
            self.state.delete_detection([5])

    def test_get_frame_detections(self):
        self.state.add_detection(Detection(frame=0, class_id=0, track_id=4, bbox=[0, 0, 100, 100]))
        self.assertEqual(len(self.state.get_frame_detections(0)), 1)
        self.assertEqual(len(self.state.get_frame_detections(1)), 0)

    def test_get_next_track_id(self):
        self.assertEqual(self.state.get_next_track_id(), 0)
        self.state.add_detection(Detection(frame=0, class_id=0, track_id=0, bbox=[0, 0, 100, 100]))
        self.assertEqual(self.state.get_next_track_id(), 1)
        self.state.add_detection(Detection(frame=0, class_id=0, track_id=1, bbox=[0, 0, 100, 100]))
        self.assertEqual(self.state.get_next_track_id(), 2)
        self.state.add_detection(Detection(frame=0, class_id=0, track_id=2, bbox=[0, 0, 100, 100]))
        self.assertEqual(self.state.get_next_track_id(), 3)
        self.state.delete_detection([1])
        self.assertEqual(self.state.get_next_track_id(), 1)
        self.state.delete_detection([0, 2])
        self.assertEqual(self.state.get_next_track_id(), 0)

if __name__ == "__main__":
    unittest.main()