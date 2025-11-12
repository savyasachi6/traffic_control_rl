"""
Convert sensor data to RL state representation.

State encoding is crucial for RL performance. This module creates
informative state vectors from sensor data that capture the essential
aspects of the traffic situation.
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional
from traffic_signal_control.core.constants import Directions, SignalState


class StateEncoder:
    """Encodes simulation state to neural network input"""
    
    TOP_K_OBJECTS = 5
    FEATURES_PER_OBJECT = 6
    SIGNAL_FEATURES = 4
    WAIT_TIME_FEATURES = 4
    EXTRA_FEATURES = 2
    TOTAL_STATE_SIZE = (
        TOP_K_OBJECTS * FEATURES_PER_OBJECT +
        SIGNAL_FEATURES +
        WAIT_TIME_FEATURES +
        EXTRA_FEATURES
    )
    
    def __init__(self, normalization: Optional[Dict] = None) -> None:
        self.normalization = normalization or {
            'max_distance': 200.0,
            'max_speed': 20.0,
            'max_wait': 120.0,
            'max_priority': 10000.0
        }
    
    def encode(self, sensor_df: pd.DataFrame, signal_state: Dict[str, str],
              approach_waits: Dict[str, float], time_in_phase: int) -> np.ndarray:
        """Encode state to array"""
        state = []
        state.extend(self._encode_top_objects(sensor_df))
        state.extend(self._encode_signal_state(signal_state))
        state.extend(self._encode_wait_times(approach_waits))
        state.extend(self._encode_extra_features(sensor_df, time_in_phase))
        
        state_array = np.array(state, dtype=np.float32)
        if len(state_array) < self.TOTAL_STATE_SIZE:
            padding = np.zeros(
                self.TOTAL_STATE_SIZE - len(state_array),
                dtype=np.float32
            )
            state_array = np.concatenate([state_array, padding])
        
        return state_array[:self.TOTAL_STATE_SIZE]
    
    def _encode_top_objects(self, df: pd.DataFrame) -> list:
        """Encode top-k objects by priority"""
        features = []
        
        if len(df) == 0:
            return [0.0] * (self.TOP_K_OBJECTS * self.FEATURES_PER_OBJECT)
        
        top_k = df.nsmallest(self.TOP_K_OBJECTS, 'priority_score')
        
        for _, obj in top_k.iterrows():
            features.append(1.0 if obj['type'] == 'pedestrian' else 0.0)
            features.append(
                self._normalize(obj['distance_m'], 0, self.normalization['max_distance'])
            )
            features.append(
                self._normalize(obj['speed_m_s'], 0, self.normalization['max_speed'])
            )
            features.append(self._normalize(obj.get('h_val', 0), 0, 50))
            features.append(
                self._normalize(obj['priority_score'], 0, self.normalization['max_priority'])
            )
            movement = obj.get('movement', 'straight')
            features.append(
                0.0 if movement == 'straight' else (0.5 if movement == 'left' else 1.0)
            )
        
        while len(features) < self.TOP_K_OBJECTS * self.FEATURES_PER_OBJECT:
            features.extend([0.0] * self.FEATURES_PER_OBJECT)
        
        return features
    
    def _encode_signal_state(self, signal_state: Dict[str, str]) -> list:
        """Encode current signal states"""
        features = []
        for direction in Directions.ALL:
            signal = signal_state.get(direction, SignalState.RED)
            features.append(1.0 if signal == SignalState.GREEN else 0.0)
        return features
    
    def _encode_wait_times(self, approach_waits: Dict[str, float]) -> list:
        """Encode wait times for each approach"""
        features = []
        for direction in Directions.ALL:
            wait = approach_waits.get(direction, 0.0)
            features.append(
                self._normalize(wait, 0, self.normalization['max_wait'])
            )
        return features
    
    def _encode_extra_features(self, df: pd.DataFrame, time_in_phase: int) -> list:
        """Encode extra features"""
        density = min(1.0, len(df) / 50.0)
        time_norm = self._normalize(time_in_phase, 0, 60)
        return [density, time_norm]
    
    @staticmethod
    def _normalize(value: float, min_val: float, max_val: float) -> float:
        """Normalize value to [0, 1]"""
        if max_val == min_val:
            return 0.5
        return float(np.clip((value - min_val) / (max_val - min_val), 0.0, 1.0))