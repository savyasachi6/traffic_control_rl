"""Training orchestration for RL agent."""

from typing import Optional, List, Dict
import numpy as np
from tqdm import tqdm
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent


class Trainer:
    """Trainer for DQN agent."""
    
    def __init__(self, env: TrafficEnv, agent: DQNAgent, 
                episodes: int = 300, batch_size: int = 32) -> None:
        self.env = env
        self.agent = agent
        self.episodes = episodes
        self.batch_size = batch_size
        self.episode_rewards: List[float] = []
    
    def train(self) -> List[float]:
        """Train agent for specified episodes"""
        print(f"\n{'='*50}")
        print(f"Starting Training: {self.episodes} episodes")
        print(f"Batch Size: {self.batch_size}")
        print(f"{'='*50}\n")
        
        for episode in tqdm(range(self.episodes), desc="Training Progress"):
            state, _ = self.env.reset()
            done = False
            truncated = False
            episode_reward = 0.0
            steps = 0
            
            while not (done or truncated):
                # Select and execute action
                action = self.agent.select_action(state, training=True)
                next_state, reward, done, truncated, info = self.env.step(action)
                episode_reward += reward
                steps += 1
                
                # Store experience
                self.agent.store_experience(state, action, reward, next_state, done)
                
                # Train on batch
                loss = self.agent.train(self.batch_size)
                
                state = next_state
            
            self.episode_rewards.append(episode_reward)
            
            # Progress reporting
            if (episode + 1) % 50 == 0:
                avg_reward = sum(self.episode_rewards[-50:]) / 50
                avg_eps = self.agent.epsilon
                print(f"  Episode {episode+1:3d} | Avg Reward: {avg_reward:7.2f} | ε: {avg_eps:.3f}")
        
        print(f"\n{'='*50}")
        print(f"✓ Training Completed!")
        print(f"Final Epsilon: {self.agent.epsilon:.4f}")
        print(f"Best Avg Reward: {max([sum(self.episode_rewards[i:i+50])/50 for i in range(0, len(self.episode_rewards)-50)]) if len(self.episode_rewards) > 50 else 0:.2f}")
        print(f"{'='*50}\n")
        
        return self.episode_rewards
