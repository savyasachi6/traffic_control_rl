"""
Multi-objective hybrid reward function.

Components:
1. r_throughput: Minimize queue lengths
2. r_fairness: Prevent starvation
3. r_safety: Prevent risky pedestrian crossings
4. r_pedestrian: Minimize pedestrian wait times
5. r_extension: Discourage excessive extensions
6. r_step: Encourage progression
7. r_rush: Reward traffic adaptation
"""

import numpy as np
import pandas as pd
from typing import Dict
import math
from traffic_signal_control.core.constants import RewardConstants
from traffic_signal_control.core.utils import MathUtils


class HybridRewardCalculator:
    """Multi-objective reward function"""
    
    def __init__(self) -> None:
        self.throughput_weight = RewardConstants.THROUGHPUT_WEIGHT
        self.fairness_weight = RewardConstants.FAIRNESS_WEIGHT
        self.safety_weight = RewardConstants.SAFETY_WEIGHT
        self.pedestrian_weight = RewardConstants.PEDESTRIAN_WEIGHT
    
    def calculate(self, queue_sizes: Dict[str, int], wait_times: Dict[str, float],
                 risky_events: int = 0, pedestrian_waiting: int = 0) -> float:
        """Calculate combined reward"""
        
        # Throughput: penalize queues
        throughput_reward = -sum(queue_sizes.values()) * self.throughput_weight
        
        # Fairness: penalize imbalance
        gini = MathUtils.gini_coefficient(list(queue_sizes.values()))
        fairness_reward = -gini * self.fairness_weight
        
        # Safety: penalize risky events
        safety_reward = -risky_events * self.safety_weight
        
        # Pedestrian: penalize waiting pedestrians
        pedestrian_reward = -pedestrian_waiting * self.pedestrian_weight
        
        # Base step penalty
        base_penalty = RewardConstants.STEP_PENALTY
        
        total_reward = (
            throughput_reward +
            fairness_reward +
            safety_reward +
            pedestrian_reward +
            base_penalty
        )
        
        return float(total_reward)
