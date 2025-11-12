from traffic_signal_control.core.constants import SimulationConstants


class PedestrianManager:
    """Manages pedestrian crossing logic"""
    
    def __init__(self) -> None:
        self.starvation_threshold = SimulationConstants.PEDESTRIAN_STARVATION_THRESHOLD
        self.crossing_speed = SimulationConstants.PEDESTRIAN_CROSSING_SPEED
        self.clearance_time = SimulationConstants.PEDESTRIAN_CLEARANCE_TIME
    
    def should_cross(self, wait_time: float, traffic_density: float) -> bool:
        """Determine if pedestrian should cross"""
        # Cross if starving or traffic is light
        return (
            wait_time > self.starvation_threshold or
            traffic_density < 0.3
        )
    
    def get_crossing_time(self, intersection_width: float = 50.0) -> float:
        """Calculate time needed to cross"""
        return (intersection_width / self.crossing_speed) + self.clearance_time
