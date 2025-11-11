"""
Abstract base class for traffic simulators.

This follows the Strategy Pattern, allowing different simulator implementations
(simple, SUMO, hybrid) while maintaining a common interface.
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Optional
import numpy as np


class BaseSimulator(ABC):
	"""
	Abstract simulator interface.
    
	Defines contract that all simulators must implement.
	"""
    
	def __init__(self, seed: int = 42):
		"""
		Initialize simulator.
        
		Args:
			seed (int): Random seed for reproducibility
		"""
		self.seed = seed
		np.random.seed(seed)
		self.current_timestep = 0
		self.spawned_count = 0
		self.cleared_count = 0
    
	@abstractmethod
	def reset(self) -> None:
		"""Reset simulator to initial state."""
		pass
    
	@abstractmethod
	def generate_timestep(self, signal_state: Dict[str, str], dt: float = 1.0) -> pd.DataFrame:
		"""
		Generate sensor data for one timestep.
        
		This is the core simulation step. Must return DataFrame with detected objects.
        
		Args:
			signal_state (Dict[str, str]): Current signal state {N: green, S: red, ...}
			dt (float): Time delta in seconds
        
		Returns:
			pd.DataFrame: Objects detected at this timestep with columns:
				- timestamp: Current timestep
				- object_id: Unique identifier
				- type: 'vehicle', 'pedestrian', or 'emergency'
				- approach: 'N', 'S', 'E', or 'W'
				- distance_m: Distance to intersection (meters)
				- speed_m_s: Speed (m/s)
				- lane: Lane number
				- movement: 'straight', 'left', or 'right'
				- f_val: A* cost (distance)
				- h_val: A* heuristic (time-to-arrival)
				- priority_score: Combined A* priority
				- committed: Is object in committed zone?
				- in_crosswalk: Is pedestrian in crosswalk?
				- wait_time: How long object has waited
		"""
		pass
    
	@abstractmethod
	def get_stats(self) -> Dict:
		"""
		Get simulation statistics.
        
		Returns:
			Dict: Statistics including:
				- spawned_count: Total objects spawned
				- cleared_count: Total objects cleared
				- current_objects: Objects currently in simulation
				- average_speed: Average vehicle speed
		"""
		pass

