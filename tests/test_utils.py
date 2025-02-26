from utils.detection import Detection

def get_dummy_detection(frame: int) -> Detection:
    return Detection(
        frame=frame,
        class_id=0,
        track_id=0
    )

