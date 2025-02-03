from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QWidget

from state import State

class ControlsWidget(QGroupBox):
    def __init__(self, central_widget: QWidget, state: State):
        super().__init__("Controls")
        self.central_widget = central_widget
        self.state = state

        layout = QVBoxLayout()
        
        self.reset_button = QPushButton("Reset All Annotations")
        self.move_to_verified_button = QPushButton("Move to Verified")
        self.move_to_new_button = QPushButton("Move to New")
        
        self.reset_button.clicked.connect(self.state.reset_annotations)
        self.move_to_verified_button.clicked.connect(self.state.move_to_verified)
        self.move_to_new_button.clicked.connect(self.state.move_to_new)
        
        layout.addWidget(self.reset_button)
        layout.addWidget(self.move_to_verified_button)
        layout.addWidget(self.move_to_new_button)
        self.setLayout(layout)