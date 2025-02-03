import os

from config import DATA_DIR

class State:
    def __init__(self):
        self.video_list = self.find_videos()
        self.current_video = self.video_list[0]
        self.current_frame = 0
        self.file_names = self.find_files(self.current_video)
    def find_videos(self) -> list[str]:
        videos = []
        for dir_name in ['new', 'verified']:
            dir_path = os.path.join(DATA_DIR, dir_name)
            if not os.path.exists(dir_path): os.makedirs(dir_path)
            subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
            for video_name in subdirs: videos.append(f"{dir_name}/{video_name}") if not video_name.startswith('.') else None
        return sorted(videos)
    
    def set_current_video(self, video_name): self.current_video = video_name; self.current_frame = 0; self.file_names = self.find_files(video_name)
    def change_frame(self, delta): self.current_frame = max(min(self.current_frame + delta, len(self.file_names) - 1), 0); self.file_names = self.find_files(self.current_video)

    def find_files(self, video_name):
        video_dir = os.path.join(DATA_DIR, video_name)
        return sorted([os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.jpg')])
    
    def reset_annotations(self): pass
    def move_to_verified(self): pass
    def move_to_new(self): pass
