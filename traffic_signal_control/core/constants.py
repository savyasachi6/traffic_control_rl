# core/constants.py - CENTRALIZED CONFIGURATION

class Directions:
    """Cardinal directions"""
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    ALL = ['N', 'S', 'E', 'W']
    
    # Opposite directions
    OPPOSITES = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }
    
    # Perpendicular directions
    PERPENDICULAR = {
        NORTH: [EAST, WEST],
        SOUTH: [EAST, WEST],
        EAST: [NORTH, SOUTH],
        WEST: [NORTH, SOUTH]
    }


class SignalState:
    """Traffic signal states"""
    GREEN = 'green'
    RED = 'red'
    ORANGE = 'orange'
    ALL_RED = 'all_red'
    
    COLORS = {
        GREEN: '#90EE90',    # Light green
        RED: '#FFB6C6',      # Light red
        ORANGE: '#FFD699',   # Light orange
        ALL_RED: '#404040'   # Dark gray
    }
    
    ICONS = {
        GREEN: '🟢',
        RED: '🔴',
        ORANGE: '🟠',
        ALL_RED: '⚫'
    }


class VehicleType:
    """Vehicle classifications"""
    REGULAR = 'vehicle'
    PEDESTRIAN = 'pedestrian'
    EMERGENCY = 'emergency'


class MovementType:
    """Turn movements"""
    STRAIGHT = 'straight'
    LEFT = 'left'
    RIGHT = 'right'


class SimulationConstants:
    """Simulation parameters"""
    # Time parameters
    BASE_GREEN_TIME = 10        # seconds
    BASE_ORANGE_TIME = 3        # seconds
    MIN_GREEN_TIME = 8          # seconds
    MAX_GREEN_TIME = 60         # seconds
    MIN_ORANGE_TIME = 3         # seconds
    
    # Pedestrian parameters
    PEDESTRIAN_CROSSING_SPEED = 1.2  # m/s
    PEDESTRIAN_CLEARANCE_TIME = 5    # seconds
    PEDESTRIAN_STARVATION_THRESHOLD = 20  # seconds
    
    # Vehicle parameters
    AVERAGE_VEHICLE_SPEED = 10  # m/s
    VEHICLE_COMMITTED_ZONE = 5  # meters
    
    # Intersection geometry
    INTERSECTION_SIZE = 50  # meters per approach
    
    # Spawn rates (vehicles per second)
    DEFAULT_SPAWN_RATE = 0.5
    DEFAULT_PED_SPAWN_RATE = 0.2
    EMERGENCY_SPAWN_RATE = 0.01
    
    # Priorities (A* bias)
    PEDESTRIAN_PRIORITY_BIAS = 20
    EMERGENCY_PRIORITY_BIAS = 10000
    LONG_WAIT_BOOST = 10  # per 10 seconds


class ActionSpace:
    """11-action space with turns"""
    # Straight traffic phases
    NS_GREEN_STRAIGHT = 0
    EW_GREEN_STRAIGHT = 1
    
    # Straight + turn phases
    NS_GREEN_WITH_LEFT = 2
    EW_GREEN_WITH_LEFT = 3
    
    # Turn-only phases
    LEFT_TURN_PHASE = 4
    
    # Pedestrian phase
    PED_CROSSING = 5
    
    # Extensions
    EXTEND_STRAIGHT = 6
    EXTEND_WITH_TURNS = 7
    
    # Advanced
    RIGHT_ON_RED_NS = 8
    RIGHT_ON_RED_EW = 9
    
    # Emergency
    EMERGENCY_OVERRIDE = 10
    
    # Total actions
    TOTAL_ACTIONS = 11
    
    DESCRIPTIONS = {
        0: "N-S Green (straight only)",
        1: "E-W Green (straight only)",
        2: "N-S Green (with left turns)",
        3: "E-W Green (with left turns)",
        4: "Left turn exclusive phase",
        5: "Pedestrian crossing",
        6: "Extend straight traffic",
        7: "Extend with turns",
        8: "Right-on-red N-S",
        9: "Right-on-red E-W",
        10: "Emergency override"
    }


class RewardConstants:
    """Multi-objective reward weights"""
    # Weights
    THROUGHPUT_WEIGHT = 1.0      # Queue reduction
    FAIRNESS_WEIGHT = 0.5        # Prevent starvation
    SAFETY_WEIGHT = 100.0        # Risky events (CRITICAL)
    PEDESTRIAN_WEIGHT = 2.0      # Pedestrian wait
    EFFICIENCY_WEIGHT = 0.2      # Time efficiency
    
    # Penalties
    RISKY_EVENT_PENALTY = -100
    STEP_PENALTY = -0.1
    EXTENSION_PENALTY = -0.2
    
    # Bonuses
    RUSH_MODE_BONUS = 5.0
    PERFECT_FAIRNESS_BONUS = 10.0


# core/utils.py - UTILITY FUNCTIONS

import numpy as np
from typing import Dict, List, Tuple

class ValidationUtils:
    """Input validation utilities"""
    
    @staticmethod
    def is_valid_direction(direction: str) -> bool:
        """Check if direction is valid"""
        return direction in Directions.ALL
    
    @staticmethod
    def is_valid_signal(signal: str) -> bool:
        """Check if signal state is valid"""
        return signal in [SignalState.GREEN, SignalState.RED, 
                         SignalState.ORANGE, SignalState.ALL_RED]
    
    @staticmethod
    def normalize_value(value: float, min_val: float, max_val: float) -> float:
        """
        Normalize value to [0, 1] range.
        
        Formula: (value - min) / (max - min)
        
        Args:
            value: Raw value
            min_val: Minimum expected value
            max_val: Maximum expected value
        
        Returns:
            Normalized value in [0, 1]
        
        Example:
            normalize_value(50, 0, 100) = 0.5
        """
        if max_val == min_val:
            return 0.0
        return (value - min_val) / (max_val - min_val)
    
    @staticmethod
    def clip_value(value: float, min_val: float, max_val: float) -> float:
        """Clip value between min and max"""
        return max(min_val, min(value, max_val))


class MathUtils:
    """Mathematical utility functions"""
    
    @staticmethod
    def gini_coefficient(values: List[float]) -> float:
        """
        Calculate Gini coefficient (measure of inequality).
        
        Range: 0 (perfect equality) to 1 (perfect inequality)
        
        Formula:
            Gini = (2 * sum(i * v_i)) / (n * sum(v_i)) - (n + 1) / n
        
        Args:
            values: List of values
        
        Returns:
            Gini coefficient
        
        Example:
            All equal: gini_coefficient([5, 5, 5]) ≈ 0.0
            Unequal: gini_coefficient([1, 5, 10]) ≈ 0.3
        """
        if len(values) == 0 or sum(values) == 0:
            return 0.0
        
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        numerator = 2 * sum((i + 1) * v for i, v in enumerate(sorted_vals))
        denominator = n * sum(sorted_vals)
        
        return max(0, (numerator / denominator) - (n + 1) / n)
    
    @staticmethod
    def exponential_decay(current_value: float, decay_rate: float, 
                         steps: int) -> float:
        """
        Calculate exponentially decayed value.
        
        Formula: value * (decay_rate ^ steps)
        
        Args:
            current_value: Starting value
            decay_rate: Decay factor (0-1)
            steps: Number of decay steps
        
        Returns:
            Decayed value
        
        Example:
            epsilon decay for exploration
        """
        return current_value * (decay_rate ** steps)
