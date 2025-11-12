#!/usr/bin/env python
"""
Console-based visualization of traffic intersection
ASCII display with real-time updates
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from traffic_signal_control.infrastructure.simulator.simulator_factory import SimulatorFactory
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent


def get_signal_icon(signal_state: str) -> str:
    """Get emoji icon for signal state"""
    icons = {
        'green': '🟢',
        'red': '🔴',
        'orange': '🟠',
        'all_red': '⚫'
    }
    return icons.get(signal_state, '⚪')


def print_intersection(step, signal_state, queue_sizes, wait_times, action, reward):
    """Print ASCII intersection visualization"""
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + "="*70)
    print(f"  🚦 TRAFFIC INTERSECTION VISUALIZATION - STEP {step}")
    print("="*70 + "\n")
    
    # Get signal icons
    n_icon = get_signal_icon(signal_state.get('N', 'red'))
    s_icon = get_signal_icon(signal_state.get('S', 'red'))
    e_icon = get_signal_icon(signal_state.get('E', 'red'))
    w_icon = get_signal_icon(signal_state.get('W', 'red'))
    
    # ASCII intersection diagram
    print(f"""
                        NORTH ({n_icon} {signal_state.get('N', 'red').upper()})
                        Queue: {queue_sizes.get('N', 0):2d} | Wait: {wait_times.get('N', 0):5.1f}s
                               ↓
            ←─────────────────┼─────────────────→
               WEST           │           EAST
         ({w_icon} {signal_state.get('W', 'red').upper():6s})  │  ({e_icon} {signal_state.get('E', 'red').upper():6s})
         Q:{queue_sizes.get('W', 0):2d} W:{wait_times.get('W', 0):5.1f}s│Q:{queue_sizes.get('E', 0):2d} W:{wait_times.get('E', 0):5.1f}s
                               ↑
                        SOUTH ({s_icon} {signal_state.get('S', 'red').upper()})
                        Queue: {queue_sizes.get('S', 0):2d} | Wait: {wait_times.get('S', 0):5.1f}s
    """)
    
    print("="*70)
    print("\n📊 AGENT DECISION:")
    action_names = {
        0: "NS_GREEN_STRAIGHT", 1: "EW_GREEN_STRAIGHT",
        2: "NS_GREEN_WITH_LEFT", 3: "EW_GREEN_WITH_LEFT",
        4: "LEFT_TURN_PHASE", 5: "PED_CROSSING",
        6: "EXTEND_STRAIGHT", 7: "EXTEND_WITH_TURNS",
        8: "RIGHT_ON_RED_NS", 9: "RIGHT_ON_RED_EW",
        10: "EMERGENCY_OVERRIDE"
    }
    
    action_name = action_names.get(action, 'UNKNOWN')
    print(f"   Action {action:2d}: {action_name}")
    print(f"   Reward: {reward:+.3f}")
    
    print("\n" + "="*70)
    print("📋 LEGEND:")
    print(f"   🟢 GREEN:  Vehicles can pass through")
    print(f"   🔴 RED:    Vehicles must stop")
    print(f"   🟠 ORANGE: Prepare to stop")
    print(f"   ⚫ ALL-RED: Pedestrian crossing")
    print("="*70 + "\n")


def main():
    """Run console visualization demo"""
    print("\n" + "="*70)
    print("  🚦 CONSOLE VISUALIZATION - TRAFFIC INTERSECTION DEMO")
    print("="*70 + "\n")
    
    try:
        # Initialize components
        print("[1/4] Initializing simulator...")
        sim = SimulatorFactory.create('simple', seed=42)
        print("      ✓ Simulator ready\n")
        
        print("[2/4] Initializing environment...")
        env = TrafficEnv(simulator=sim, config={'max_steps_per_episode': 50})
        print("      ✓ Environment ready\n")
        
        print("[3/4] Initializing DQN agent...")
        agent = DQNAgent(state_size=env.observation_space.shape[0], action_size=11)
        print("      ✓ Agent ready\n")
        
        print("[4/4] Starting simulation (Press Ctrl+C to stop)...\n")
        input("Press ENTER to start visualization...")
        
        # Run simulation with visualization
        state, _ = env.reset()
        signal_state = {'N': 'green', 'S': 'red', 'E': 'red', 'W': 'red'}
        total_reward = 0.0
        
        for step in range(50):
            # Get action
            action = agent.select_action(state, training=False)
            
            # Step environment
            next_state, reward, done, truncated, info = env.step(action)
            total_reward += reward
            
            # Update for visualization
            queue_sizes = info.get('queue_sizes', {'N': 0, 'S': 0, 'E': 0, 'W': 0})
            wait_times = info.get('wait_times', {'N': 0, 'S': 0, 'E': 0, 'W': 0})
            
            # Cycle through signal states for demo
            if step % 10 == 0:
                signal_state = {'N': 'green', 'S': 'red', 'E': 'red', 'W': 'red'}
            elif step % 10 == 5:
                signal_state = {'N': 'orange', 'S': 'orange', 'E': 'green', 'W': 'green'}
            
            # Print visualization
            print_intersection(step, signal_state, queue_sizes, wait_times, action, reward)
            
            state = next_state
            
            # User input for next step
            if step < 49:
                input("Press ENTER for next step...")
            
            if done or truncated:
                print(f"\n✓ Episode finished at step {step+1}")
                break
        
        # Final summary
        print("\n" + "="*70)
        print("  SIMULATION SUMMARY")
        print("="*70)
        print(f"Total Steps: {step+1}")
        print(f"Total Reward: {total_reward:.3f}")
        print(f"Average Reward/Step: {total_reward/(step+1):.3f}")
        print("="*70 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n✓ Simulation stopped by user")
        return 0
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
