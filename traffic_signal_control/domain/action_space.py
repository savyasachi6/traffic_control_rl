"""
Action space definitions (re-export from core for convenience).

This is primarily in core.constants, but re-exported here for domain logic.
"""

from ..core import ActionSpace
from typing import Dict
from traffic_signal_control.core.constants import ActionSpace as ActionSpaceConstants


class ActionHandler:
    """Handles action mapping and execution"""

    ACTION_MAP = ActionSpaceConstants.DESCRIPTIONS

    @staticmethod
    def get_action_name(action_id: int) -> str:
        """Get name of action"""
        if action_id not in ActionHandler.ACTION_MAP:
            return "UNKNOWN"
        return ActionHandler.ACTION_MAP[action_id]

    @staticmethod
    def get_action_duration(action_id: int, queue_size: int) -> int:
        """Get duration for action"""
        base_duration = 10

        if action_id in [6, 7]:  # Extension actions
            return base_duration + min(queue_size * 2, 20)
        elif action_id == 5:  # Pedestrian crossing
            return 8

        return base_duration

    @staticmethod
    def is_valid_action(action_id: int) -> bool:
        """Validate action ID"""
        return 0 <= action_id < 11

__all__ = ["ActionSpace", "ActionHandler"]
