"""
OpenAI Gym-compatible traffic environment.

Interface between RL agent and simulator.
Handles:
- State encoding
- Action execution
- Reward calculation
- Episode management
"""

import gymnasium as gym
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, Optional
from traffic_signal_control.infrastructure.simulator.simulator_factory import SimulatorFactory
from traffic_signal_control.infrastructure.environment.state_encoder import StateEncoder
from traffic_signal_control.infrastructure.environment.signal_controller import SignalController
from traffic_signal_control.core.constants import Directions


class TrafficEnv(gym.Env):
    """Traffic control environment compatible with Gymnasium"""
    
    metadata = {'render_modes': ['human'], 'render_fps': 10}
    
    def __init__(self, simulator=None, config: Optional[Dict] = None) -> None:
        """Initialize environment"""
        self.config = config or {'max_steps_per_episode': 200}
        
        if simulator is None:
            simulator = SimulatorFactory.create('simple')
        self.simulator = simulator
        
        self.state_encoder = StateEncoder()
        self.signal_controller = SignalController()
        
        self.action_space = gym.spaces.Discrete(11)
        self.observation_space = gym.spaces.Box(
            low=0.0,
            high=1.0,
            shape=(self.state_encoder.TOTAL_STATE_SIZE,),
            dtype=np.float32
        )
        
        self.max_steps = self.config.get('max_steps_per_episode', 200)
        self.step_count = 0
        self.total_reward = 0.0
        self.last_sensor_df = pd.DataFrame()
        self.episode_step_rewards = []
    
    def reset(self, seed: Optional[int] = None, 
             options: Optional[Dict] = None) -> Tuple[np.ndarray, Dict]:
        """Reset environment - Gymnasium API"""
        super().reset(seed=seed)
        
        if seed is not None:
            np.random.seed(seed)
            self.simulator.seed = seed
        
        self.simulator.reset()
        self.signal_controller.reset()
        self.step_count = 0
        self.total_reward = 0.0
        self.episode_step_rewards = []
        self.last_sensor_df = pd.DataFrame()
        
        return self._get_state(), {}
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """Execute one step - Gymnasium API"""
        if not isinstance(action, (int, np.integer)):
            action = int(action)
        
        if not self.action_space.contains(action):
            raise ValueError(f"Invalid action: {action}")
        
        self.step_count += 1
        
        # Get current signal state
        signal_state = self.signal_controller.get_signal_state()
        
        # Generate timestep data
        self.last_sensor_df = self.simulator.generate_timestep(signal_state, dt=1.0)
        
        # Calculate reward
        reward = self._compute_reward(self.last_sensor_df)
        self.total_reward += reward
        self.episode_step_rewards.append(reward)
        
        # Check termination
        done = self.step_count >= self.max_steps
        truncated = False
        
        # Collect info
        info = {
            'step': self.step_count,
            'total_reward': self.total_reward,
            'avg_reward': np.mean(self.episode_step_rewards) if self.episode_step_rewards else 0.0,
            'queue_sizes': self._get_queue_sizes(self.last_sensor_df),
            'wait_times': self._get_wait_times(self.last_sensor_df),
        }
        
        return self._get_state(), float(reward), done, truncated, info
    
    def _get_state(self) -> np.ndarray:
        """Get current state observation"""
        signal_state = self.signal_controller.get_signal_state()
        approach_waits = {d: 0.0 for d in Directions.ALL}
        time_in_phase = int(self.signal_controller.time_in_phase)
        
        if not self.last_sensor_df.empty:
            approach_waits = self._get_wait_times(self.last_sensor_df)
        
        return self.state_encoder.encode(
            self.last_sensor_df, 
            signal_state, 
            approach_waits, 
            time_in_phase
        )
    
    def _compute_reward(self, df: pd.DataFrame) -> float:
        """Compute step reward"""
        reward = -0.1  # Base step penalty
        
        if len(df) > 0:
            # Penalize queue length
            reward -= len(df) * 0.01
            
            # Bonus for low wait times
            if 'wait_time' in df.columns:
                avg_wait = df['wait_time'].mean()
                if avg_wait < 5.0:
                    reward += 0.05
        
        return reward
    
    def _get_queue_sizes(self, df: pd.DataFrame) -> Dict[str, int]:
        """Get vehicle count per approach"""
        if df.empty:
            return {d: 0 for d in Directions.ALL}
        
        queue_sizes = {}
        for direction in Directions.ALL:
            queue_sizes[direction] = len(
                df[(df['approach'] == direction) & (df['type'] == 'vehicle')]
            )
        return queue_sizes
    
    def _get_wait_times(self, df: pd.DataFrame) -> Dict[str, float]:
        """Get average wait time per approach"""
        if df.empty:
            return {d: 0.0 for d in Directions.ALL}
        
        wait_times = {}
        for direction in Directions.ALL:
            approach_df = df[df['approach'] == direction]
            if len(approach_df) > 0:
                wait_times[direction] = float(approach_df['wait_time'].mean())
            else:
                wait_times[direction] = 0.0
        return wait_times
    
    def render(self) -> None:
        """Render environment (placeholder)"""
        pass
    
    def close(self) -> None:
        """Clean up resources"""
        pass
