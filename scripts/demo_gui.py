#!/usr/bin/env python
"""
PyQt5 GUI-based visualization with corrected QPainter usage
Professional interactive interface
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QSlider, QStatusBar
    )
    from PyQt5.QtGui import QFont
    from PyQt5.QtCore import Qt, QTimer
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False
    print("Error: PyQt5 not installed")
    print("Install with: pip install PyQt5")
    sys.exit(1)

from traffic_signal_control.presentation.gui.intersection_widget import IntersectionWidget
from traffic_signal_control.infrastructure.simulator.simulator_factory import SimulatorFactory
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent


class SimulationWindow(QMainWindow):
    """Main window for GUI simulation"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚦 Traffic Signal Control - GUI Visualization")
        self.setGeometry(100, 100, 1200, 700)
        
        # Initialize simulation components
        try:
            self.sim = SimulatorFactory.create('simple', seed=42)
            self.env = TrafficEnv(self.sim, config={'max_steps_per_episode': 200})
            self.agent = DQNAgent(state_size=self.env.observation_space.shape[0], action_size=11)
        except Exception as e:
            print(f"Error initializing simulation: {e}")
            sys.exit(1)
        
        self.state, _ = self.env.reset()
        self.step_count = 0
        self.total_reward = 0.0
        self.is_running = False
        
        # Timer for simulation
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulation_step)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left side: Intersection visualization
        left_layout = QVBoxLayout()
        self.intersection_widget = IntersectionWidget()
        left_layout.addWidget(self.intersection_widget)
        
        # Right side: Controls and info
        right_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("🚦 Traffic Signal Control")
        title_font = QFont("Arial", 14, QFont.Bold)
        title_label.setFont(title_font)
        right_layout.addWidget(title_label)
        
        # Status info
        self.status_info = QLabel("Status: Ready\nStep: 0\nReward: 0.00")
        info_font = QFont("Courier", 10)
        self.status_info.setFont(info_font)
        right_layout.addWidget(self.status_info)
        
        # Controls
        controls_layout = QVBoxLayout()
        
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.clicked.connect(self.play_simulation)
        controls_layout.addWidget(self.play_btn)
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.clicked.connect(self.pause_simulation)
        self.pause_btn.setEnabled(False)
        controls_layout.addWidget(self.pause_btn)
        
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self.reset_simulation)
        controls_layout.addWidget(self.reset_btn)
        
        self.step_btn = QPushButton("⏭ Next Step")
        self.step_btn.clicked.connect(self.simulation_step)
        controls_layout.addWidget(self.step_btn)
        
        right_layout.addLayout(controls_layout)
        
        # Speed control
        speed_label = QLabel("Simulation Speed:")
        right_layout.addWidget(speed_label)
        
        speed_layout = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(100)
        self.speed_slider.setMaximum(2000)
        self.speed_slider.setValue(500)
        self.speed_slider.valueChanged.connect(self.update_speed)
        speed_layout.addWidget(self.speed_slider)
        
        self.speed_label = QLabel("500ms")
        speed_layout.addWidget(self.speed_label)
        right_layout.addLayout(speed_layout)
        
        right_layout.addStretch()
        
        # Combine layouts
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Status bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")
    
    def play_simulation(self):
        """Start simulation"""
        self.is_running = True
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.step_btn.setEnabled(False)
        self.timer.start(self.speed_slider.value())
        self.statusBar().showMessage("Running...")
    
    def pause_simulation(self):
        """Pause simulation"""
        self.is_running = False
        self.timer.stop()
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.step_btn.setEnabled(True)
        self.statusBar().showMessage("Paused")
    
    def reset_simulation(self):
        """Reset simulation"""
        self.timer.stop()
        self.state, _ = self.env.reset()
        self.step_count = 0
        self.total_reward = 0.0
        self.is_running = False
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.step_btn.setEnabled(True)
        self.update_display()
        self.statusBar().showMessage("Reset")
    
    def simulation_step(self):
        """Execute one simulation step"""
        if self.step_count >= 200:
            self.pause_simulation()
            self.statusBar().showMessage("Episode Complete")
            return
        
        # Get action
        action = self.agent.select_action(self.state, training=False)
        
        # Step environment
        self.state, reward, done, truncated, info = self.env.step(action)
        
        self.step_count += 1
        self.total_reward += reward
        
        # Update display
        self.update_display()
        
        if done or truncated:
            self.pause_simulation()
            self.statusBar().showMessage("Episode Complete")
    
    def update_display(self):
        """Update UI display"""
        # Cycle signal states for demo
        if self.step_count % 15 == 0:
            signal_state = {'N': 'green', 'S': 'red', 'E': 'red', 'W': 'red'}
        elif self.step_count % 15 == 10:
            signal_state = {'N': 'orange', 'S': 'orange', 'E': 'green', 'W': 'green'}
        else:
            signal_state = {'N': 'red', 'S': 'green', 'E': 'red', 'W': 'red'}
        
        # Generate demo queues (decreasing as they pass through)
        queue_sizes = {
            'N': max(0, 3 - self.step_count // 5),
            'S': 1,
            'E': 2,
            'W': 1
        }
        
        wait_times = {'N': 0, 'S': 5, 'E': 3, 'W': 3}
        
        # Update intersection widget
        self.intersection_widget.update_state(signal_state, queue_sizes, wait_times, self.step_count)
        
        # Update status info
        avg_reward = self.total_reward / max(1, self.step_count)
        status_text = (
            f"Status: Running\n"
            f"Step: {self.step_count}\n"
            f"Reward: {self.total_reward:+.2f}\n"
            f"Avg: {avg_reward:+.3f}"
        )
        self.status_info.setText(status_text)
    
    def update_speed(self, value):
        """Update simulation speed"""
        self.speed_label.setText(f"{value}ms")
        if self.is_running:
            self.timer.setInterval(value)
    
    def closeEvent(self, event):
        """Handle window close"""
        self.timer.stop()
        event.accept()


def main():
    """Run GUI demo"""
    print("\n" + "="*70)
    print("  🚦 PyQt5 GUI VISUALIZATION - TRAFFIC INTERSECTION DEMO")
    print("="*70 + "\n")
    
    try:
        app = QApplication(sys.argv)
        window = SimulationWindow()
        window.show()
        
        print("✓ GUI window opened")
        print("✓ Use buttons to control simulation")
        print("✓ Close window to exit\n")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
