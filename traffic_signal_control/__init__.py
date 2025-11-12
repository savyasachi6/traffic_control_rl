"""
Traffic Signal Control: Deep RL-based traffic signal optimization system
"""
__version__ = "0.2.0"
__author__ = "Traffic Control Research"

# Core modules
from traffic_signal_control.core.constants import (
    Directions, SignalState, ActionSpace
)

__all__ = [
    "Directions", "SignalState", "ActionSpace",
    "__version__", "__author__"
]
