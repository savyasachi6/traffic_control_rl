"""
PyQt5 widget for intersection visualization
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt


class IntersectionWidget(QWidget):
    """PyQt5 widget for rendering intersection"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signal_state = {'N': 'red', 'S': 'red', 'E': 'red', 'W': 'red'}
        self.queues = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        self.wait_times = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        self.step = 0
        
        self.setMinimumSize(600, 600)
        self.setStyleSheet("background-color: white;")
    
    def paintEvent(self, event):
        """Draw intersection"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w, h = self.width(), self.height()
        center_x, center_y = w // 2, h // 2
        road_width = 100
        
        # Draw roads (light gray)
        painter.fillRect(0, center_y - road_width//2, w, road_width, QColor(200, 200, 200))
        painter.fillRect(center_x - road_width//2, 0, road_width, h, QColor(200, 200, 200))
        
        # Draw road markings (yellow dashed lines)
        painter.setPen(QPen(QColor(255, 255, 0), 2, Qt.DashLine))
        painter.drawLine(center_x, center_y - road_width//2, center_x, center_y - 60)
        painter.drawLine(center_x, center_y + road_width//2, center_x, center_y + 60)
        painter.drawLine(center_x - road_width//2, center_y, center_x - 60, center_y)
        painter.drawLine(center_x + road_width//2, center_y, center_x + 60, center_y)
        
        # Draw intersection (dark gray)
        painter.setBrush(QColor(100, 100, 100))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawRect(center_x - 50, center_y - 50, 100, 100)
        
        # Draw approaches with signals and vehicles
        self._draw_approach(painter, center_x, center_y - 150, 'N', 'up')
        self._draw_approach(painter, center_x, center_y + 150, 'S', 'down')
        self._draw_approach(painter, center_x - 150, center_y, 'W', 'left')
        self._draw_approach(painter, center_x + 150, center_y, 'E', 'right')
        
        # Draw step counter
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(10, 20, f"Step: {self.step}")
        
        # Draw legend
        painter.setFont(QFont("Arial", 10))
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(10, h - 20, "🟢 Green | 🔴 Red | 🟠 Orange | ⚫ All-Red")
    
    def _draw_approach(self, painter, x, y, direction, orientation):
        """Draw one approach (N/S/E/W)"""
        signal_colors = {
            'green': QColor(0, 255, 0),
            'red': QColor(255, 0, 0),
            'orange': QColor(255, 165, 0),
            'all_red': QColor(0, 0, 0)
        }
        
        signal = self.signal_state.get(direction, 'red')
        queue = self.queues.get(direction, 0)
        wait = self.wait_times.get(direction, 0)
        
        # Draw signal light (circle) - FIXED: Use setBrush + drawEllipse
        painter.setBrush(signal_colors[signal])
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(x - 15, y - 15, 30, 30)
        
        # Draw info text
        font = QFont("Arial", 9)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(x - 40, y + 40, f"Q:{queue} W:{wait:.1f}s")
        
        # Draw vehicles (small rectangles)
        painter.setBrush(QColor(0, 0, 255))
        painter.setPen(QPen(QColor(0, 0, 100), 1))
        
        if orientation == 'up':
            for i in range(min(queue, 3)):
                painter.drawRect(x - 8, y - 50 - i*15, 16, 12)
        elif orientation == 'down':
            for i in range(min(queue, 3)):
                painter.drawRect(x - 8, y + 50 + i*15, 16, 12)
        elif orientation == 'left':
            for i in range(min(queue, 3)):
                painter.drawRect(x - 50 - i*15, y - 8, 12, 16)
        elif orientation == 'right':
            for i in range(min(queue, 3)):
                painter.drawRect(x + 50 + i*15, y - 8, 12, 16)
    
    def update_state(self, signal_state, queues, wait_times, step):
        """Update display state"""
        self.signal_state = signal_state
        self.queues = queues
        self.wait_times = wait_times
        self.step = step
        self.update()


__all__ = ['IntersectionWidget']
