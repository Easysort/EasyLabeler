from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget
from PyQt5.QtGui import QColor

from state import State

class VideoListWidget(QListWidget):
    def __init__(self, central_widget: QWidget, state: State):
        super().__init__()
        self._state = state
        self.central_widget = central_widget
        self.load_videos()
        self.itemClicked.connect(self.on_list_clicked)
        self.setFixedWidth(270)

    def load_videos(self):
        self.clear()
        self.addItem("--- New ---")
        for video_name in self._state.video_list:
            if video_name.startswith("new/"):
                item = QListWidgetItem(video_name.replace("new/", ""))
                if self._state.current_video and video_name == self._state.current_video: item.setBackground(QColor('lightblue'))
                self.addItem(item)

        self.addItem("--- Verified ---")
        for video_name in self._state.video_list:
            if video_name.startswith("verified/"):
                item = QListWidgetItem(video_name.replace("verified/", ""))
                item.setForeground(QColor('green'))
                if self._state.current_video and video_name == self._state.current_video: item.setBackground(QColor('lightblue'))
                self.addItem(item)

    def on_list_clicked(self, item: QListWidgetItem):
        if not item.text().startswith("---"):
            clicked_name = item.text()
            for video_name in self._state.video_list:
                if video_name.endswith("/" + clicked_name):
                    self._state.set_current_video(video_name)
                    self.on_video_change()
                    break

    def on_video_change(self):
        self.load_videos()
        self.central_widget.reload_image()