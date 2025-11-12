from typing import Dict


class TrafficPatternManager:
    """Manages time-of-day traffic patterns"""

    def __init__(self) -> None:
        self.patterns = {
            "early_morning": (0, 6, 0.1),      # Low traffic
            "morning_rush": (6, 9, 1.5),       # High traffic
            "midday": (9, 15, 0.6),            # Medium traffic
            "evening_rush": (15, 18, 1.5),     # High traffic
            "night": (18, 24, 0.3),            # Low traffic
        }

    def get_spawn_rate(self, hour: int, base_rate: float = 0.5) -> float:
        """Get spawn rate multiplier for hour"""
        for period, (start, end, multiplier) in self.patterns.items():
            if start <= hour < end:
                return base_rate * multiplier
        return base_rate

    def get_turn_distribution(self, hour: int) -> Dict[str, float]:
        """Get distribution of turn movements"""
        # More left turns during rush hours
        if 6 <= hour < 9 or 15 <= hour < 18:
            return {"straight": 0.7, "left": 0.15, "right": 0.15}
        return {"straight": 0.8, "left": 0.1, "right": 0.1}
