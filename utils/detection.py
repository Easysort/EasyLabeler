import numpy as np
from utils.classes import DEFAULT_CLASS_NAMES, DEFAULT_COLORS, DEFAULT_CLASS_TO_FRACTION, DEFAULT_FRACTIONS

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
    def corners(self) -> list[np.ndarray]:
        return [np.array([self.x1, self.y1]), np.array([self.x2, self.y1]), np.array([self.x1, self.y2]), np.array([self.x2, self.y2])]
    def to_json(self) -> list: return self.xywh().tolist()
    def to_dict(self) -> dict: return {"x": self.pos[0], "y": self.pos[1], "w": self.size[0], "h": self.size[1]}
    def copy(self) -> "Bbox": return Bbox(*self.to_json())
    def __repr__(self) -> str: return "Bbox(x={}, y={}, w={}, h={})".format(self.pos[0], self.pos[1], self.size[0], self.size[1])
    def __eq__(self, other: "Bbox") -> bool: return np.allclose(self.pos, other.pos) and np.allclose(self.size, other.size)

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

    def is_near_point(self, x: float, y: float, scale: float = 1.0, threshold: float = 10.0) -> bool:
        return any(np.linalg.norm(corner - (np.array([x, y]) * scale)) < threshold for corner in self.bbox.corners())

    def __eq__(self, other: "Detection") -> bool:
        return self.frame == other.frame and self.track_id == other.track_id and self.class_id == other.class_id and self.bbox == other.bbox

    # Class handling:
    @property
    def class_name(self) -> str: return DEFAULT_CLASS_NAMES[self.class_id]

    @property
    def color(self) -> tuple[int, int, int]: return DEFAULT_COLORS[self.class_id]

    def move_class_id_up(self):
        next_id = self.class_id + 1
        while next_id not in DEFAULT_CLASS_NAMES:
            next_id += 1
            if next_id > max(DEFAULT_CLASS_NAMES.keys()):
                next_id = min(DEFAULT_CLASS_NAMES.keys())
        self.class_id = next_id

    def move_class_id_down(self):
        prev_id = self.class_id - 1
        while prev_id not in DEFAULT_CLASS_NAMES:
            prev_id -= 1
            if prev_id < min(DEFAULT_CLASS_NAMES.keys()):
                prev_id = max(DEFAULT_CLASS_NAMES.keys())
        self.class_id = prev_id

    def move_class_id_up_fraction(self):
        self.class_id = DEFAULT_FRACTIONS[0 if DEFAULT_CLASS_TO_FRACTION[self.class_id] + 1 >= len(DEFAULT_FRACTIONS)
                                          else DEFAULT_CLASS_TO_FRACTION[self.class_id] + 1]
    def move_class_id_down_fraction(self):
        self.class_id = DEFAULT_FRACTIONS[len(DEFAULT_FRACTIONS) - 1 if DEFAULT_CLASS_TO_FRACTION[self.class_id] - 1 < 0
                                          else DEFAULT_CLASS_TO_FRACTION[self.class_id] - 1]
