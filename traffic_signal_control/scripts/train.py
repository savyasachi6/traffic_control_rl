"""
train.py: Headless RL agent training for traffic control
"""
from traffic_signal_control.infrastructure.simulator import SimulatorFactory
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent
from traffic_signal_control.application.trainer import Trainer

sim = SimulatorFactory.create('simple', seed=42)
env = TrafficEnv(simulator=sim, config={'max_steps_per_episode':200})
agent = DQNAgent(state_size=env.state_encoder.TOTAL_STATE_SIZE, action_size=11)
trainer = Trainer(env, agent, episodes=300)
trainer.train()
