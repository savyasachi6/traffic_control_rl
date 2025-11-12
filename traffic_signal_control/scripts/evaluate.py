"""
evaluate.py: Run systematic policy evaluation and print/report metrics.
"""
from traffic_signal_control.infrastructure.simulator import SimulatorFactory
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent
from traffic_signal_control.application.evaluator import evaluate_agent

sim = SimulatorFactory.create('simple', seed=17)
env = TrafficEnv(simulator=sim, config={'max_steps_per_episode':100})
agent = DQNAgent.load("outputs/models/final_model.pth")
scores = evaluate_agent(env, agent, episodes=10)
print(f"Evaluation results (rewards): {scores}")
