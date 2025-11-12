"""
Deep Q-Network agent for traffic signal control.

Double DQN with experience replay and target network.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Optional
from traffic_signal_control.infrastructure.agent.replay_buffer import ReplayBuffer


class DQNNetwork(nn.Module):
    """Deep Q-Network for traffic signal control"""
    
    def __init__(self, state_size: int, action_size: int, hidden_size: int = 128) -> None:
        super().__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)
        self.relu = nn.ReLU()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)


class DQNAgent:
    """Double DQN Agent with GPU/CPU support"""
    
    def __init__(self, state_size: int, action_size: int, 
                learning_rate: float = 0.001, gamma: float = 0.99,
                device: Optional[str] = None) -> None:
        """
        Initialize agent
        
        Args:
            state_size: Size of state space
            action_size: Number of actions
            learning_rate: Learning rate
            gamma: Discount factor
            device: 'cuda', 'cpu', or None (auto-detect)
        """
        # Device setup
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        print(f"[DQNAgent] Using device: {self.device}")
        
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        
        # Networks
        self.model = DQNNetwork(state_size, action_size).to(self.device)
        self.target_model = DQNNetwork(state_size, action_size).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()
        
        # Optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()
        
        # Replay buffer
        self.replay_buffer = ReplayBuffer(capacity=10000)
        
        # Exploration
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        
        self.update_counter = 0
        self.target_update_freq = 100
    
    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Select action using epsilon-greedy policy"""
        if training and np.random.random() < self.epsilon:
            return np.random.randint(0, self.action_size)
        
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            q_values = self.model(state_tensor)
        
        return q_values.argmax(dim=1).item()
    
    def store_experience(self, state: np.ndarray, action: int, 
                        reward: float, next_state: np.ndarray, done: bool) -> None:
        """Store experience in replay buffer"""
        self.replay_buffer.push(state, action, reward, next_state, done)
    
    def train(self, batch_size: int = 32) -> Optional[float]:
        """Train on a batch"""
        if len(self.replay_buffer) < batch_size:
            return None
        
        # Sample batch
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(batch_size)
        
        # Convert to tensors
        states_t = torch.FloatTensor(states).to(self.device)
        actions_t = torch.LongTensor(actions).to(self.device)
        rewards_t = torch.FloatTensor(rewards).to(self.device)
        next_states_t = torch.FloatTensor(next_states).to(self.device)
        dones_t = torch.FloatTensor(dones).to(self.device)
        
        # Current Q values
        q_values = self.model(states_t).gather(1, actions_t.unsqueeze(1)).squeeze(1)
        
        # Target Q values (Double DQN)
        with torch.no_grad():
            next_actions = self.model(next_states_t).argmax(dim=1)
            next_q_values = self.target_model(next_states_t).gather(
                1, next_actions.unsqueeze(1)
            ).squeeze(1)
            target_q_values = rewards_t + (1 - dones_t) * self.gamma * next_q_values
        
        # Compute loss
        loss = self.criterion(q_values, target_q_values)
        
        # Backward pass
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()
        
        # Update target network
        self.update_counter += 1
        if self.update_counter % self.target_update_freq == 0:
            self.target_model.load_state_dict(self.model.state_dict())
        
        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        return float(loss.item())
    
    def save_model(self, path: str) -> None:
        """Save model checkpoint"""
        torch.save({
            'model_state': self.model.state_dict(),
            'target_state': self.target_model.state_dict(),
            'epsilon': self.epsilon,
            'optimizer_state': self.optimizer.state_dict()
        }, path)
        print(f"✓ Model saved to {path}")
    
    def load_model(self, path: str) -> None:
        """Load model checkpoint"""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state'])
        self.target_model.load_state_dict(checkpoint.get('target_state', checkpoint['model_state']))
        self.epsilon = checkpoint.get('epsilon', 0.01)
        if 'optimizer_state' in checkpoint:
            self.optimizer.load_state_dict(checkpoint['optimizer_state'])
        print(f"✓ Model loaded from {path}")
