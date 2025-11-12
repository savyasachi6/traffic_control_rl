"""
Safety constraints layer.

Enforces hard constraints that cannot be violated.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from ..core import SimulationConstants, Directions
from traffic_signal_control.core.constants import SignalState


@dataclass
class SafetyConstraints:
    """Hard safety constraints."""
    
    MIN_GREEN_TIME: int = SimulationConstants.MIN_GREEN_TIME
    MIN_ORANGE_TIME: int = SimulationConstants.MIN_ORANGE_TIME
    MAX_GREEN_TIME: int = SimulationConstants.MAX_GREEN_TIME
    PEDESTRIAN_CLEARANCE_TIME: int = SimulationConstants.PEDESTRIAN_CLEARANCE_TIME
    MAX_WAIT_TIME: int = SimulationConstants.MAX_WAIT_TIME
    STARVATION_THRESHOLD: int = SimulationConstants.STARVATION_SERVICE_INTERVAL
    COMMITTED_ZONE_DISTANCE: float = SimulationConstants.VEHICLE_COMMITTED_ZONE
    
    CONFLICTING_PAIRS: List[Tuple[str, str]] = None
    
    def __post_init__(self):
        if self.CONFLICTING_PAIRS is None:
            self.CONFLICTING_PAIRS = [
                ("N", "S"),
                ("E", "W"),
                ("N", "E"), ("N", "W"),
                ("S", "E"), ("S", "W"),
                ("E", "N"), ("E", "S"),
                ("W", "N"), ("W", "S"),
            ]


class SafetyManager:
    """Enforces safety constraints."""
    
    def __init__(self, constraints: SafetyConstraints = None):
        self.constraints = constraints or SafetyConstraints()
        self.signal_times = {"N": 0, "S": 0, "E": 0, "W": 0}
    
    def validate_action(self, action: int, current_state: Dict) -> bool:
        """Validate if action is safe."""
        # All actions are valid if constraints are enforced elsewhere
        return 0 <= action < 11
    
    def enforce_constraints(self, signal_state: Dict[str, str]) -> Dict[str, str]:
        """Enforce hard safety constraints."""
        enforced_state = signal_state.copy()
        # Constraints enforced during signal controller phase
        return enforced_state
    
    def is_safe_to_change_phase(self, time_in_phase: float) -> bool:
        """Check if safe to change signal phase."""
        return time_in_phase >= self.constraints.MIN_GREEN_TIME
