"""Policy evaluation module"""
from typing import List, Dict
import numpy as np
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent


class Evaluator:
    """Evaluates trained policy"""
    
    @staticmethod
    def evaluate(env: TrafficEnv, agent: DQNAgent, 
                episodes: int = 10) -> List[float]:
        """Evaluate policy over episodes"""
        stats: List[float] = []
        
        for episode in range(episodes):
            state, _ = env.reset()
            done = False
            truncated = False
            total_reward = 0.0
            
            while not (done or truncated):
                action = agent.select_action(state, training=False)
                state, reward, done, truncated, info = env.step(action)
                total_reward += reward
            
            stats.append(total_reward)
        
        return stats
    
    @staticmethod
    def get_statistics(rewards: List[float]) -> Dict:
        """Calculate statistics from rewards"""
        rewards_array = np.array(rewards)
        
        return {
            'mean': float(np.mean(rewards_array)),
            'std': float(np.std(rewards_array)),
            'min': float(np.min(rewards_array)),
            'max': float(np.max(rewards_array)),
            'median': float(np.median(rewards_array)),
        }
