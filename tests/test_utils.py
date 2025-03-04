from utils.detection import Detection
import shutil
from pathlib import Path

def get_dummy_detection(frame: int, track_id: int = 0) -> Detection:
    return Detection(
        frame=frame,
        class_id=0,
        track_id=track_id
    )

class UniversalCleanup:
    def __init__(self): self.files_to_delete = []
    def add_file(self, file: Path | str): self.files_to_delete.append(file)
    def cleanup(self): [shutil.rmtree(file) if file.is_dir() else file.unlink() for file in self.files_to_delete if file.exists()]