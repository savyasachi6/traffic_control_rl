"""
Reusable PyQt5 widgets.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class IntersectionWidget(QWidget):
    """Widget displaying intersection state."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status_label = QLabel("Initializing...", self)
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        self.setLayout(layout)
    
    def update_state(self, state_dict):
        """Update widget with new state."""
        self.status_label.setText(str(state_dict))
