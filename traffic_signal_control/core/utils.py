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