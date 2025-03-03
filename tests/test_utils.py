from utils.detection import Detection

def get_dummy_detection(frame: int, track_id: int = 0) -> Detection:
    return Detection(
        frame=frame,
        class_id=0,
        track_id=track_id
    )

