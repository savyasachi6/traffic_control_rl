"""
Abstract base class for traffic simulators.
Defines interface all simulators must implement.
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Optional
import numpy as np


class BaseSimulator(ABC):
    """Abstract simulator interface"""
    
    def __init__(self, seed: int = 42) -> None:
        """Initialize simulator"""
        self.seed = seed
        np.random.seed(seed)
        self.current_timestep: int = 0
        self.spawned_count: int = 0
        self.cleared_count: int = 0
    
    @abstractmethod
    def reset(self) -> None:
        """Reset simulator to initial state"""
        pass
    
    @abstractmethod
    def generate_timestep(self, signal_state: Dict[str, str], 
                         dt: float = 1.0) -> pd.DataFrame:
        """
        Generate sensor data for one timestep.
        
        Args:
            signal_state: Current signal states {N: green, S: red, ...}
            dt: Time delta in seconds
        
        Returns:
            DataFrame with detected objects
        """
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict:
        """Get simulation statistics"""
        pass

