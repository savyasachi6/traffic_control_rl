"""
Signal controller managing traffic light state and transitions.

Handles:
- Signal state management
- Phase transitions
- Timing enforcement
- Conflict prevention
"""

from typing import Dict
from traffic_signal_control.core.constants import Directions, SignalState


class SignalController:
    """Manages traffic signal states and timing"""
    
    def __init__(self) -> None:
        self.signal_state: Dict[str, str] = {d: SignalState.RED for d in Directions.ALL}
        self.time_in_phase: float = 0.0
        self.phase_duration: float = 0.0
        self.phase_history: list = []
    
    def get_signal_state(self) -> Dict[str, str]:
        """Get current signal state"""
        return self.signal_state.copy()
    
    def set_signal(self, direction: str, state: str, duration: float) -> None:
        """Set signal for direction"""
        if direction not in Directions.ALL:
            raise ValueError(f"Invalid direction: {direction}")
        if state not in [SignalState.GREEN, SignalState.RED, SignalState.ORANGE]:
            raise ValueError(f"Invalid signal state: {state}")
        
        self.signal_state[direction] = state
        self.phase_duration = duration
        self.time_in_phase = 0.0
    
    def update(self, dt: float = 1.0) -> None:
        """Update signal timing"""
        self.time_in_phase += dt
        if self.time_in_phase >= self.phase_duration:
            self.time_in_phase = self.phase_duration
    
    def is_phase_complete(self) -> bool:
        """Check if current phase is complete"""
        return self.time_in_phase >= self.phase_duration
    
    def reset(self) -> None:
        """Reset to initial state"""
        self.signal_state = {d: SignalState.RED for d in Directions.ALL}
        self.time_in_phase = 0.0
        self.phase_duration = 0.0
        self.phase_history.clear()
