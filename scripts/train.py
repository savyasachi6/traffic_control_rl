#!/usr/bin/env python
"""Headless training script"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from traffic_signal_control.infrastructure.simulator.simulator_factory import SimulatorFactory
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent
from traffic_signal_control.application.trainer import Trainer


def main():
    """Run training"""
    print("\n" + "="*70)
    print("  🚦 TRAFFIC SIGNAL CONTROL - TRAINING")
    print("="*70 + "\n")
    
    try:
        # Setup
        print("[1/4] Setting up simulator...")
        sim = SimulatorFactory.create('simple', seed=42)
        print("      ✓ Simulator ready\n")
        
        print("[2/4] Setting up environment...")
        env = TrafficEnv(simulator=sim, config={'max_steps_per_episode': 200})
        print("      ✓ Environment ready\n")
        
        print("[3/4] Initializing agent...")
        agent = DQNAgent(state_size=env.observation_space.shape[0], action_size=11)
        print("      ✓ Agent ready\n")
        
        print("[4/4] Starting training...\n")
        trainer = Trainer(env, agent, episodes=300, batch_size=32)
        rewards = trainer.train()
        
        print("\n" + "="*70)
        print("✓ Training completed!")
        print("="*70 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
