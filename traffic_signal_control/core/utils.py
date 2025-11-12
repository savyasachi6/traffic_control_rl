"""
Utility functions: normalization, validation, helpers
"""
from typing import List, Dict, Tuple, Any
import numpy as np
from traffic_signal_control.core.constants import Directions, SignalState


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
        """
        if max_val == min_val:
            return 0.5
        normalized = (value - min_val) / (max_val - min_val)
        return np.clip(float(normalized), 0.0, 1.0)
    
    @staticmethod
    def clip_value(value: float, min_val: float, max_val: float) -> float:
        """Clip value between min and max"""
        return float(np.clip(value, min_val, max_val))


class MathUtils:
    """Mathematical utility functions"""
    
    @staticmethod
    def gini_coefficient(values: List[float]) -> float:
        """
        Calculate Gini coefficient (inequality measure).
        Range: 0 (perfect equality) to 1 (perfect inequality)
        """
        if len(values) == 0:
            return 0.0
        
        values = np.array(values, dtype=float)
        if np.sum(values) == 0:
            return 0.0
        
        sorted_vals = np.sort(values)
        n = len(sorted_vals)
        numerator = 2 * np.sum((np.arange(1, n + 1)) * sorted_vals)
        denominator = n * np.sum(sorted_vals)
        
        gini = (numerator / denominator) - (n + 1) / n
        return float(np.clip(gini, 0.0, 1.0))
    
    @staticmethod
    def exponential_decay(current_value: float, decay_rate: float, 
                         steps: int) -> float:
        """Calculate exponentially decayed value"""
        return float(current_value * (decay_rate ** steps))
    
    @staticmethod
    def moving_average(values: List[float], window: int) -> List[float]:
        """Calculate moving average"""
        if len(values) < window:
            return values
        
        values_array = np.array(values, dtype=float)
        result = np.convolve(values_array, np.ones(window) / window, mode='valid')
        return result.tolist()
    

class NormalizationUtils:
    """Normalization and scaling utilities."""
    
    @staticmethod
    def min_max_normalize(value: float, min_val: float, max_val: float) -> float:
        """
        Min-max normalization to [0, 1] range.
        
        Formula: (value - min) / (max - min)
        
        Args:
            value: Raw value to normalize
            min_val: Minimum expected value
            max_val: Maximum expected value
        
        Returns:
            Normalized value in [0, 1]
        
        Example:
            >>> NormalizationUtils.min_max_normalize(50, 0, 100)
            0.5
        """
        if max_val == min_val:
            return 0.5
        return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
    
    @staticmethod
    def z_score_normalize(value: float, mean: float, std_dev: float) -> float:
        """
        Z-score (standard) normalization.
        
        Formula: (value - mean) / std_dev
        Range: approximately [-3, 3]
        
        Args:
            value: Raw value
            mean: Mean of distribution
            std_dev: Standard deviation
        
        Returns:
            Z-score normalized value
        """
        if std_dev == 0:
            return 0.0
        return (value - mean) / std_dev
    
    @staticmethod
    def log_normalize(value: float, base: float = 10) -> float:
        """
        Logarithmic normalization for large value ranges.
        
        Formula: log_base(value + 1)
        
        Args:
            value: Value to normalize (must be >= 0)
            base: Logarithm base (default 10)
        
        Returns:
            Logarithmically scaled value
        """
        if value < 0:
            return 0.0
        return float(np.log(value + 1) / np.log(base))
    
    @staticmethod
    def sigmoid_normalize(value: float, steepness: float = 1.0, center: float = 0.5) -> float:
        """
        Sigmoid (S-curve) normalization.
        
        Formula: 1 / (1 + exp(-steepness * (value - center)))
        Range: (0, 1)
        
        Args:
            value: Raw value
            steepness: Curve steepness (higher = sharper transition)
            center: Center point of transition
        
        Returns:
            Sigmoid-normalized value in (0, 1)
        """
        try:
            return float(1.0 / (1.0 + np.exp(-steepness * (value - center))))
        except OverflowError:
            return 1.0 if value > center else 0.0


# Convenience functions (aliases for backward compatibility)
def normalize(value: float, minimum: float, maximum: float) -> float:
    """
    Min-max normalization shorthand.
    
    Args:
        value: Raw value
        minimum: Min boundary
        maximum: Max boundary
    
    Returns:
        Normalized value [0, 1]
    """
    return NormalizationUtils.min_max_normalize(value, minimum, maximum)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value to [min_value, max_value] range.
    
    Args:
        value: Value to clamp
        min_value: Minimum allowed
        max_value: Maximum allowed
    
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def clip(value: float, lower: float, upper: float) -> float:
    """Alias for clamp."""
    return clamp(value, lower, upper)
