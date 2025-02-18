
import numpy as np

class Bbox:
    def __init__(self, x: float = 0, y: float = 0, w: float = 0, h: float = 0):
        self.pos = np.array([x, y], dtype=float)
        self.size = np.array([w, h], dtype=float)

    def resize(self, scale: float) -> None:
        self.pos *= scale
        self.size *= scale
    def __bool__(self) -> bool: return bool(np.any(self.pos) or np.any(self.size))
    def center(self) -> np.ndarray: return self.pos + self.size / 2
    def xywh(self) -> np.ndarray: return np.concatenate([self.pos, self.size])
    def set_x1(self, x1: float) -> None:
        self.size[0] += (self.pos[0] - x1)
        self.pos[0] = x1
    def set_y1(self, y1: float) -> None:
        self.size[1] += (self.pos[1] - y1)
        self.pos[1] = y1
    def set_x2(self, x2: float) -> None: self.size[0] += (x2 - self.pos[0] - self.size[0])
    def set_y2(self, y2: float) -> None: self.size[1] += (y2 - self.pos[1] - self.size[1])
    def to_json(self) -> list: return self.xywh().tolist()
    def to_dict(self) -> dict: return {"x": self.pos[0], "y": self.pos[1], "w": self.size[0], "h": self.size[1]}
    def copy(self) -> "Bbox": return Bbox(*self.to_json())
    def __repr__(self) -> str: return "Bbox(x={}, y={}, w={}, h={})".format(self.pos[0], self.pos[1], self.size[0], self.size[1])

    @property
    def x1(self) -> float: return self.pos[0]
    @property
    def y1(self) -> float: return self.pos[1]
    @property
    def x2(self) -> float: return self.pos[0] + self.size[0]
    @property
    def y2(self) -> float: return self.pos[1] + self.size[1]

class Detection:
    def __init__(self, frame: int, class_id: int = 0, track_id: int = 0, bbox: Bbox | list[float] = Bbox()):
        self.frame = frame
        self.class_id = class_id
        self.track_id = track_id
        assert isinstance(bbox, Bbox) or isinstance(bbox, list) and len(bbox) == 4, "bbox must be a Bbox or a list of 4 floats"
        self.bbox = bbox if isinstance(bbox, Bbox) else Bbox(*bbox)

    @staticmethod
    def from_json(data: dict) -> "Detection": return Detection(data["frame"], data["class_id"], data["track_id"], Bbox(*data["bbox"]))
    def __repr__(self) -> str: return f"Detection(frame={self.frame}, class_id={self.class_id}, track_id={self.track_id}, bbox={self.bbox})"

    def to_json(self) -> dict:
        return {
            "frame": self.frame,
            "track_id": self.track_id,
            "class_id": self.class_id,
            "bbox": self.bbox.to_json()
        }