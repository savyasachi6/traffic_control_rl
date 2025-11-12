#!/usr/bin/env python
"""
Matplotlib-based real-time visualization
Shows intersection with vehicles and metrics plots
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from traffic_signal_control.infrastructure.simulator.simulator_factory import SimulatorFactory
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent


class IntersectionVisualizer:
    """Real-time matplotlib visualization"""
    
    def __init__(self):
        self.fig, (self.ax_intersection, self.ax_metrics) = plt.subplots(
            1, 2, figsize=(14, 6)
        )
        self.rewards = []
        self.wait_times_ns = []
        self.wait_times_ew = []
        self.queue_sizes_ns = []
        self.queue_sizes_ew = []
        self.step_count = 0
    
    def draw_intersection(self, signal_state, queues, step):
        """Draw intersection with signals and vehicles"""
        self.ax_intersection.clear()
        
        # Draw road grid
        road_color = (200/255, 200/255, 200/255)
        self.ax_intersection.add_patch(
            patches.Rectangle((0, 40), 100, 20, facecolor=road_color, edgecolor='black')
        )
        self.ax_intersection.add_patch(
            patches.Rectangle((40, 0), 20, 100, facecolor=road_color, edgecolor='black')
        )
        
        # Draw intersection center
        self.ax_intersection.add_patch(
            patches.Rectangle((40, 40), 20, 20, facecolor=(100/255, 100/255, 100/255), 
                            edgecolor='black', linewidth=2)
        )
        
        # Signal colors
        signal_colors = {
            'green': 'green',
            'red': 'red',
            'orange': 'orange',
            'all_red': 'black'
        }
        
        # North signal
        n_signal = signal_state.get('N', 'red')
        circle_n = patches.Circle((50, 75), 3, color=signal_colors.get(n_signal, 'gray'))
        self.ax_intersection.add_patch(circle_n)
        self.ax_intersection.text(50, 82, f"N\n{n_signal.upper()}\nQ:{queues.get('N', 0)}", 
                                ha='center', fontsize=9, fontweight='bold')
        
        # South signal
        s_signal = signal_state.get('S', 'red')
        circle_s = patches.Circle((50, 25), 3, color=signal_colors.get(s_signal, 'gray'))
        self.ax_intersection.add_patch(circle_s)
        self.ax_intersection.text(50, 12, f"S\n{s_signal.upper()}\nQ:{queues.get('S', 0)}", 
                                ha='center', fontsize=9, fontweight='bold')
        
        # East signal
        e_signal = signal_state.get('E', 'red')
        circle_e = patches.Circle((75, 50), 3, color=signal_colors.get(e_signal, 'gray'))
        self.ax_intersection.add_patch(circle_e)
        self.ax_intersection.text(88, 50, f"E\n{e_signal.upper()}\nQ:{queues.get('E', 0)}", 
                                ha='center', fontsize=9, fontweight='bold')
        
        # West signal
        w_signal = signal_state.get('W', 'red')
        circle_w = patches.Circle((25, 50), 3, color=signal_colors.get(w_signal, 'gray'))
        self.ax_intersection.add_patch(circle_w)
        self.ax_intersection.text(12, 50, f"W\n{w_signal.upper()}\nQ:{queues.get('W', 0)}", 
                                ha='center', fontsize=9, fontweight='bold')
        
        # Draw vehicles as rectangles
        # North approach
        for i in range(min(queues.get('N', 0), 5)):
            vehicle = patches.Rectangle((48, 60 - i*3), 4, 2, color='blue', alpha=0.7)
            self.ax_intersection.add_patch(vehicle)
        
        # South approach
        for i in range(min(queues.get('S', 0), 5)):
            vehicle = patches.Rectangle((48, 35 + i*3), 4, 2, color='blue', alpha=0.7)
            self.ax_intersection.add_patch(vehicle)
        
        # East approach
        for i in range(min(queues.get('E', 0), 5)):
            vehicle = patches.Rectangle((60 + i*3, 48), 2, 4, color='blue', alpha=0.7)
            self.ax_intersection.add_patch(vehicle)
        
        # West approach
        for i in range(min(queues.get('W', 0), 5)):
            vehicle = patches.Rectangle((35 - i*3, 48), 2, 4, color='blue', alpha=0.7)
            self.ax_intersection.add_patch(vehicle)
        
        self.ax_intersection.set_xlim(-5, 105)
        self.ax_intersection.set_ylim(-5, 105)
        self.ax_intersection.set_aspect('equal')
        self.ax_intersection.set_title(f'Intersection Status (Step {step})', 
                                      fontsize=14, fontweight='bold')
        self.ax_intersection.axis('off')
    
    def draw_metrics(self):
        """Draw performance metrics"""
        self.ax_metrics.clear()
        
        if len(self.rewards) > 0:
            x = np.arange(len(self.rewards))
            self.ax_metrics.plot(x, self.rewards, label='Reward', marker='o', markersize=4, linewidth=2)
            self.ax_metrics.plot(x, self.wait_times_ns, label='Wait (N-S)', marker='s', markersize=4)
            self.ax_metrics.plot(x, self.wait_times_ew, label='Wait (E-W)', marker='^', markersize=4)
            
            self.ax_metrics.set_xlabel('Timestep', fontweight='bold')
            self.ax_metrics.set_ylabel('Value', fontweight='bold')
            self.ax_metrics.set_title('Performance Metrics', fontweight='bold', fontsize=12)
            self.ax_metrics.legend(loc='best')
            self.ax_metrics.grid(True, alpha=0.3)
    
    def update(self, signal_state, queues, reward, wait_times, step):
        """Update visualization"""
        self.draw_intersection(signal_state, queues, step)
        
        self.rewards.append(reward)
        self.wait_times_ns.append(wait_times.get('N', 0) + wait_times.get('S', 0))
        self.wait_times_ew.append(wait_times.get('E', 0) + wait_times.get('W', 0))
        self.queue_sizes_ns.append(queues.get('N', 0) + queues.get('S', 0))
        self.queue_sizes_ew.append(queues.get('E', 0) + queues.get('W', 0))
        
        self.draw_metrics()
        plt.tight_layout()
        plt.pause(0.5)


def main():
    """Run matplotlib visualization demo"""
    print("\n" + "="*70)
    print("  🚦 MATPLOTLIB VISUALIZATION - TRAFFIC INTERSECTION DEMO")
    print("="*70 + "\n")
    
    try:
        # Initialize
        print("[1/4] Initializing simulator...")
        sim = SimulatorFactory.create('simple', seed=42)
        print("      ✓ Simulator ready\n")
        
        print("[2/4] Initializing environment...")
        env = TrafficEnv(simulator=sim, config={'max_steps_per_episode': 50})
        print("      ✓ Environment ready\n")
        
        print("[3/4] Initializing DQN agent...")
        agent = DQNAgent(state_size=env.observation_space.shape[0], action_size=11)
        print("      ✓ Agent ready\n")
        
        print("[4/4] Starting visualization...\n")
        print("Close the matplotlib window to exit.\n")
        
        visualizer = IntersectionVisualizer()
        plt.ion()  # Interactive mode
        
        state, _ = env.reset()
        
        # Simulate with visualization
        signal_state = {'N': 'green', 'S': 'red', 'E': 'red', 'W': 'red'}
        queue_sizes = {'N': 3, 'S': 1, 'E': 2, 'W': 1}
        wait_times = {'N': 0, 'S': 5, 'E': 3, 'W': 3}
        
        for step in range(50):
            # Update state
            queue_sizes['N'] = max(0, queue_sizes['N'] - 1) if signal_state['N'] == 'green' else min(queue_sizes['N'] + 1, 10)
            queue_sizes['S'] = max(0, queue_sizes['S'] - 1) if signal_state['S'] == 'green' else min(queue_sizes['S'] + 1, 10)
            
            # Get action
            action = agent.select_action(state, training=False)
            state, reward, done, truncated, info = env.step(action)
            
            # Cycle signals
            if step % 15 == 0:
                signal_state = {'N': 'green', 'S': 'red', 'E': 'red', 'W': 'red'}
            elif step % 15 == 10:
                signal_state = {'N': 'orange', 'S': 'orange', 'E': 'green', 'W': 'green'}
            
            # Update visualization
            visualizer.update(signal_state, queue_sizes, reward, wait_times, step)
            
            if done or truncated:
                print(f"\n✓ Episode finished at step {step+1}")
                break
        
        print("\nClose the plot window to exit.")
        plt.show()
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
