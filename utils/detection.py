
import numpy as np


class Bbox:
    def __init__(self, x=0, y=0, w=0, h=0): self.pos = np.array([x, y], dtype=float); self.size = np.array([w, h], dtype=float)
    
    @staticmethod
    def get_thickness(): return 2

    @staticmethod
    def get_anchor_size(): return 4 * Bbox.get_thickness()
    
    def resize(self, scale): self.pos *= scale; self.size *= scale; return self
    def __bool__(self): return bool(np.any(self.pos) or np.any(self.size))

    @property
    def xywh(self):
        return np.concatenate([self.pos, self.size])

    @property
    def x1y1x2y2(self):
        return np.concatenate([self.pos, self.pos + self.size])

    @property
    def xcycwh(self):
        return np.concatenate([self.center, self.size])

    @property
    def center(self):
        return self.pos + self.size / 2

    def set_x1(self, x1): self.size[0] += (self.pos[0] - x1); self.pos[0] = x1
    def set_y1(self, y1): self.size[1] += (self.pos[1] - y1); self.pos[1] = y1
    def set_x2(self, x2): self.size[0] += (x2 - self.pos[0] - self.size[0])
    def set_y2(self, y2): self.size[1] += (y2 - self.pos[1] - self.size[1])

    @staticmethod
    def from_center_size(center, size): bbox = Bbox(); bbox.pos = center - size / 2; bbox.size = size; return bbox

    def correct_negative_size(self):
        if self.size[0] < 0: self.size[0] *= -1; self.pos[0] -= self.size[0]
        if self.size[1] < 0: self.size[1] *= -1; self.pos[1] -= self.size[1]

    def to_json(self): return self.xywh.tolist()
    def to_dict(self): x, y, w, h = self.xywh; return {"x": x, "y": y, "w": w, "h": h}
    def copy(self): return Bbox(*self.to_json())
    def __repr__(self): return "Bbox(x={}, y={}, w={}, h={})".format(self.pos[0], self.pos[1], self.size[0], self.size[1])

    ## ANCHORS ##

    # def get_anchors(self, factor=2):
    #     anchors = {}

    #     xmin, ymin, xmax, ymax = self.x1y1x2y2
    #     mid_x, mid_y = (xmin + xmax) / 2, (ymin + ymax) / 2

    #     sRA = Bbox.get_thickness() * factor

    #     L_ = [xmin - sRA, xmin + sRA]
    #     M_ = [mid_x - sRA, mid_x + sRA]
    #     R_ = [xmax - sRA, xmax + sRA]
    #     _T = [ymin - sRA, ymin + sRA]
    #     _M = [mid_y - sRA, mid_y + sRA]
    #     _B = [ymax - sRA, ymax + sRA]

    #     anchors['LT'] = [L_[0], _T[0], L_[1], _T[1]]
    #     anchors['MT'] = [M_[0], _T[0], M_[1], _T[1]]
    #     anchors['RT'] = [R_[0], _T[0], R_[1], _T[1]]
    #     anchors['LM'] = [L_[0], _M[0], L_[1], _M[1]]
    #     anchors['RM'] = [R_[0], _M[0], R_[1], _M[1]]
    #     anchors['LB'] = [L_[0], _B[0], L_[1], _B[1]]
    #     anchors['MB'] = [M_[0], _B[0], M_[1], _B[1]]
    #     anchors['RB'] = [R_[0], _B[0], R_[1], _B[1]]

    #     return anchors

    # def intersects(self, anchor):
    #     xmin, ymin, xmax, ymax = self.x1y1x2y2
    #     xA = max(xmin, anchor[0])
    #     yA = max(ymin, anchor[1])
    #     xB = min(xmax, anchor[2])
    #     yB = min(ymax, anchor[3])

    #     return max(0, xB - xA + 1) * max(0, yB - yA + 1) > 0

    # def is_inside(self, p):
    #     xmin, ymin, xmax, ymax = self.x1y1x2y2
    #     return xmin <= p[0] <= xmax and ymin <= p[1] <= ymax

    # def is_inside_anchors(self, p):
    #     for anchor_key, anchor in self.get_anchors().items():
    #         xmin, ymin, xmax, ymax = anchor
    #         if xmin <= p[0] <= xmax and ymin <= p[1] <= ymax:
    #             return True, anchor_key
    #     return False, ""

class Detection:
    def __init__(self, frame, class_id=0, track_id=0, bbox=Bbox()):
        self.frame = frame
        self.class_id = class_id
        self.track_id = track_id
        self.bbox = bbox

    @staticmethod
    def from_json(data):
        return Detection(data["frame"], data["class_id"], data["track_id"], Bbox(*data["bbox"]))

    def to_json(self):
        return {
            "frame": self.frame,
            "track_id": self.track_id,
            "class_id": self.class_id,
            "bbox": self.bbox.to_json()
        }