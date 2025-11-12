"""Domain Layer (Layer 3): Business logic and traffic control algorithms.

Exports:
- RewardCalculator: Multi-objective reward function
- SafetyManager: Hard constraint enforcement
- PedestrianManager: Pedestrian safety logic
- TurnManager: Turn movement handling
- TrafficPatternManager: Dynamic traffic patterns
- ActionSpace: Action definitions (also in core, re-exported here)
"""

from . import action_space
from . import reward_calculator
from . import safety_manager
from . import pedestrian_manager
from . import turn_manager
from . import traffic_patterns

# Re-export primary domain classes for easy importing
from .reward_calculator import RewardCalculator
from .safety_manager import SafetyManager
from .pedestrian_manager import PedestrianManager
from .turn_manager import TurnManager
from .traffic_patterns import TrafficPatternManager
from .action_space import ActionSpace

__all__ = [
    "action_space",
    "reward_calculator",
    "safety_manager",
    "pedestrian_manager",
    "turn_manager",
    "traffic_patterns",
    "RewardCalculator",
    "SafetyManager",
    "PedestrianManager",
    "TurnManager",
    "TrafficPatternManager",
    "ActionSpace",
]

"""Domain layer: Business logic"""
from traffic_signal_control.domain.reward_calculator import HybridRewardCalculator
from traffic_signal_control.domain.safety_manager import SafetyManager
from traffic_signal_control.domain.pedestrian_manager import PedestrianManager
from traffic_signal_control.domain.turn_manager import TurnManager
from traffic_signal_control.domain.traffic_patterns import TrafficPatternManager
from traffic_signal_control.domain.action_space import ActionHandler

__all__ = [
    "HybridRewardCalculator", "SafetyManager", "PedestrianManager",
    "TurnManager", "TrafficPatternManager", "ActionHandler",
]
