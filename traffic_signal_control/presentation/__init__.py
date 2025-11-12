"""Presentation layer: GUI and visualization"""
try:
    from traffic_signal_control.presentation.gui.main_window import MainWindow
    __all__ = ['MainWindow']
except ImportError:
    __all__ = []
