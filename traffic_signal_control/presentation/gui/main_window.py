"""
PyQt5 GUI for traffic signal control system
"""
try:
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
        QLabel, QPushButton, QStatusBar, QSlider, QSpinBox
    )
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QFont
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False


class MainWindow(QMainWindow):
    """Main GUI window for traffic control"""
    
    def __init__(self) -> None:
        if not PYQT5_AVAILABLE:
            raise ImportError("PyQt5 not installed. Install with: pip install PyQt5")
        
        super().__init__()
        self.setWindowTitle("🚦 Traffic Signal Control System")
        self.setGeometry(100, 100, 1000, 700)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup UI components"""
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🚦 Traffic Signal Control - Deep RL System")
        title_font = QFont("Arial", 16, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Main content layout
        content_layout = QHBoxLayout()
        
        # Left side: Visualization placeholder
        left_layout = QVBoxLayout()
        visualization_label = QLabel("Intersection Visualization Area")
        visualization_label.setStyleSheet("border: 2px solid #ccc; padding: 20px;")
        visualization_label.setMinimumHeight(400)
        left_layout.addWidget(visualization_label)
        
        # Right side: Controls
        right_layout = QVBoxLayout()
        
        # Status display
        self.status_info = QLabel("Status: Ready\nStep: 0\nReward: 0.00")
        info_font = QFont("Courier", 10)
        self.status_info.setFont(info_font)
        right_layout.addWidget(self.status_info)
        
        right_layout.addSpacing(10)
        
        # Control buttons
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.clicked.connect(self._on_play)
        right_layout.addWidget(self.play_btn)
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.clicked.connect(self._on_pause)
        self.pause_btn.setEnabled(False)
        right_layout.addWidget(self.pause_btn)
        
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self._on_reset)
        right_layout.addWidget(self.reset_btn)
        
        self.step_btn = QPushButton("⏭ Next Step")
        self.step_btn.clicked.connect(self._on_step)
        right_layout.addWidget(self.step_btn)
        
        right_layout.addSpacing(10)
        
        # Speed control
        speed_label = QLabel("Simulation Speed:")
        right_layout.addWidget(speed_label)
        
        speed_layout = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(100)
        self.speed_slider.setMaximum(2000)
        self.speed_slider.setValue(500)
        self.speed_slider.valueChanged.connect(self._update_speed_display)
        speed_layout.addWidget(self.speed_slider)
        
        self.speed_label = QLabel("500ms")
        self.speed_label.setMaximumWidth(50)
        speed_layout.addWidget(self.speed_label)
        right_layout.addLayout(speed_layout)
        
        right_layout.addStretch()
        
        # Combine layouts
        content_layout.addLayout(left_layout, 2)
        content_layout.addLayout(right_layout, 1)
        
        layout.addLayout(content_layout)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Status bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")
    
    def _on_play(self) -> None:
        """Handle play button"""
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.statusBar().showMessage("Running...")
    
    def _on_pause(self) -> None:
        """Handle pause button"""
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.statusBar().showMessage("Paused")
    
    def _on_reset(self) -> None:
        """Handle reset button"""
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.status_info.setText("Status: Ready\nStep: 0\nReward: 0.00")
        self.statusBar().showMessage("Reset")
    
    def _on_step(self) -> None:
        """Handle step button"""
        self.statusBar().showMessage("Step executed")
    
    def _update_speed_display(self, value: int) -> None:
        """Update speed display"""
        self.speed_label.setText(f"{value}ms")


def launch_gui_trainer() -> None:
    """Launch GUI trainer"""
    if not PYQT5_AVAILABLE:
        print("Error: PyQt5 not installed. Install with: pip install PyQt5")
        return
    
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


def launch_gui_demo() -> None:
    """Launch GUI demo"""
    if not PYQT5_AVAILABLE:
        print("Error: PyQt5 not installed. Install with: pip install PyQt5")
        return
    
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
