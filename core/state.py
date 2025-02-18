import os
import json
from PyQt5.QtWidgets import QWidget
from typing import List

from config import DATA_DIR
from utils.detection import Detection

class State:
    def __init__(self, central_widget: QWidget):
        self.central_widget = central_widget
        self.video_list = self.find_videos()
        self.current_video = self.video_list[0]
        self.current_frame = 0
        self.file_names = self.find_files(self.current_video)
        self.detections = self.load_annotations()
        self.frame_to_detections = {} # TODO: Optimize using frame_to_detections when drawing detections

    def find_videos(self) -> list[str]:
        videos = []
        for dir_name in ['new', 'verified']:
            dir_path = os.path.join(DATA_DIR, dir_name)
            if not os.path.exists(dir_path): os.makedirs(dir_path)
            subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
            for video_name in subdirs: videos.append(f"{dir_name}/{video_name}") if not video_name.startswith('.') else None
        return sorted(videos)

    def set_current_video(self, video_name):
        self.current_video = video_name
        self.current_frame = 0
        self.file_names = self.find_files(video_name)
        self.detections = self.load_annotations()

    def change_frame(self, delta):
        self.current_frame = max(min(self.current_frame + delta, len(self.file_names) - 1), 0)
        self.file_names = self.find_files(self.current_video)

    def find_files(self, video_name):
        video_dir = os.path.join(DATA_DIR, video_name)
        return sorted([os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.jpg')])

    def reset_annotations(self): self.detections = {}
    def move_to_verified(self):
        self.move_folder(
            os.path.join(DATA_DIR, self.current_video.split("/")[-1]),
            os.path.join(DATA_DIR, 'verified', self.current_video.split("/")[-1])
        )

    def move_to_new(self):
        self.move_folder(
            os.path.join(DATA_DIR, self.current_video.split("/")[-1]),
            os.path.join(DATA_DIR, 'new', self.current_video.split("/")[-1])
        )

    def move_folder(self, old_path, new_path):
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        os.rename(old_path, new_path)

    def load_annotations(self) -> dict:
        if not os.path.exists(os.path.join(DATA_DIR, self.current_video, 'annotations.json')): return {}
        with open(os.path.join(DATA_DIR, self.current_video, 'annotations.json')) as f:
            self.detections = {k: Detection.from_json(v) for k,v in json.load(f).items()}

    def save_annotations(self):
        if self.detections:
            path = os.path.join(DATA_DIR, self.current_video, 'annotations.json')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f: json.dump({k: v.to_json() for k,v in self.detections.items()}, f, indent=2)

    def delete_detection(self, track_ids: List[int]):
        assert all(_id in self.detections for _id in track_ids), f"Detection ids: {[_id for _id in track_ids if _id in self.detections]} do not exist"
        self.detections = {k: v for k, v in self.detections.items() if k not in track_ids}

    def add_detection(self, detection: Detection):
        assert detection.track_id not in self.detections, f"Detection with track id {detection.track_id} already exists"
        self.detections[detection.track_id] = detection

    def update_detection(self, detection: Detection):
        assert detection.track_id in self.detections, f"Detection with track id {detection.track_id} does not exist, use add_detection instead"
        self.detections[detection.track_id] = detection

    @property
    def num_detections(self) -> int: return len(self.detections)

    def get_frame_detections(self, frame_idx: int) -> List[Detection]:
        return [v for k,v in self.detections.items() if v.frame == frame_idx] # TODO: Slow, maybe optimize with frame_to_detections
