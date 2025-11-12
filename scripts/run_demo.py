#!/usr/bin/env python
"""
Quick demo of traffic signal control system
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_dependencies():
    """Check all required dependencies"""
    dependencies = {
        'numpy': 'numpy',
        'pandas': 'pandas',
        'torch': 'torch',
        'gymnasium': 'gymnasium',
    }
    
    missing = []
    for name, package in dependencies.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing


def main():
    """Run demo"""
    print("\n" + "="*70)
    print("  🚦 TRAFFIC SIGNAL CONTROL - QUICK DEMO")
    print("="*70 + "\n")
    
    # Check dependencies
    print("[0/5] Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print(f"      ✗ Missing: {', '.join(missing)}")
        print("\n      Fix: Run these commands:")
        print(f"      pip install {' '.join(missing)}")
        return 1
    print("      ✓ All dependencies found\n")
    
    try:
        # Initialize simulator
        print("[1/5] Initializing simulator...")
        from traffic_signal_control.infrastructure.simulator.simulator_factory import SimulatorFactory
        sim = SimulatorFactory.create('simple', seed=42)
        print("      ✓ Simulator ready\n")
        
        # Initialize environment
        print("[2/5] Initializing environment...")
        from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
        env = TrafficEnv(simulator=sim, config={'max_steps_per_episode': 50})
        print(f"      ✓ Environment ready (State size: {env.observation_space.shape[0]})\n")
        
        # Initialize agent
        print("[3/5] Initializing DQN agent...")
        from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent
        agent = DQNAgent(
            state_size=env.observation_space.shape[0],
            action_size=11
        )
        print("      ✓ Agent ready\n")
        
        # Run demo
        print("[4/5] Running 10 demo steps...\n")
        state, _ = env.reset()
        total_reward = 0.0
        
        action_names = {
            0: "NS_GREEN_STRAIGHT", 1: "EW_GREEN_STRAIGHT",
            2: "NS_GREEN_WITH_LEFT", 3: "EW_GREEN_WITH_LEFT",
            4: "LEFT_TURN_PHASE", 5: "PED_CROSSING",
            6: "EXTEND_STRAIGHT", 7: "EXTEND_WITH_TURNS",
            8: "RIGHT_ON_RED_NS", 9: "RIGHT_ON_RED_EW",
            10: "EMERGENCY_OVERRIDE"
        }
        
        for step in range(10):
            action = agent.select_action(state, training=False)
            next_state, reward, done, truncated, info = env.step(action)
            total_reward += reward
            
            queue_sizes = info['queue_sizes']
            action_name = action_names.get(action, 'UNKNOWN')
            
            print(f"  Step {step+1:2d} | Action: {action:2d} ({action_name:20s}) | "
                  f"Reward: {reward:7.3f} | "
                  f"Queues: N={queue_sizes['N']} S={queue_sizes['S']} "
                  f"E={queue_sizes['E']} W={queue_sizes['W']}")
            
            state = next_state
            if done or truncated:
                break
        
        print(f"\n  Total Reward: {total_reward:.3f}")
        
        print("\n[5/5] Verification")
        print(f"      ✓ Simulator stats: {sim.get_stats()}")
        
        print("\n" + "="*70)
        print("  ✓ Demo completed successfully!")
        print("="*70 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
