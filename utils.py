import os
import datetime

def get_free_filename(date_str = None, frames_folders = ["data/new", "data/verified"]):
    """
    Returns a filename for a file that should be followed by the current date,
    but if this is already in the frames folder, then iterate by 1, until
    you have a free file name.
    """
    base_filename = "d"
    date_str = datetime.date.today().strftime("%Y-%m-%d") if date_str is None else date_str
    base_filename_with_date = f"{base_filename}_{date_str}"

    i = 0
    while True:
        if not any([os.path.exists(os.path.join(frames_folder, f"{base_filename_with_date}_{i}")) for frames_folder in frames_folders]):
            return os.path.join("data", "new", f"{base_filename_with_date}_{i}")
        i += 1
