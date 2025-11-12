from traffic_signal_control.core.constants import SignalState


class TurnManager:
    """Manages turn logic and yielding"""

    def calculate_left_turn_wait(self, opposing_signal: str, opposing_queue: int) -> float:
        """Calculate wait time for left turn based on opposing traffic"""
        if opposing_signal == SignalState.GREEN:
            return 15.0 + opposing_queue * 2.0
        return 0.0

    def is_safe_to_turn(self, opposing_signal: str) -> bool:
        """Check if safe to make left turn"""
        return opposing_signal != SignalState.GREEN
