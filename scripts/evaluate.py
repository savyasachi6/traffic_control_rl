#!/usr/bin/env python
"""Policy evaluation script"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from traffic_signal_control.infrastructure.simulator.simulator_factory import SimulatorFactory
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent
from traffic_signal_control.application.evaluator import Evaluator


def main():
    """Evaluate policy"""
    print("\n" + "="*70)
    print("  🚦 TRAFFIC SIGNAL CONTROL - EVALUATION")
    print("="*70 + "\n")
    
    try:
        print("[1/3] Setting up environment...")
        sim = SimulatorFactory.create('simple', seed=17)
        env = TrafficEnv(simulator=sim, config={'max_steps_per_episode': 100})
        print("      ✓ Environment ready\n")
        
        print("[2/3] Creating agent...")
        agent = DQNAgent(state_size=env.observation_space.shape[0], action_size=11)
        print("      ✓ Agent ready\n")
        
        print("[3/3] Running evaluation (10 episodes)...\n")
        scores = Evaluator.evaluate(env, agent, episodes=10)
        stats = Evaluator.get_statistics(scores)
        
        print("\nResults:")
        print(f"  Mean:   {stats['mean']:7.3f}")
        print(f"  Std:    {stats['std']:7.3f}")
        print(f"  Min:    {stats['min']:7.3f}")
        print(f"  Max:    {stats['max']:7.3f}")
        print(f"  Median: {stats['median']:7.3f}")
        
        print("\n" + "="*70)
        print("✓ Evaluation completed!")
        print("="*70 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
