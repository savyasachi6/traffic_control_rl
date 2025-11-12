import os

# Define the folder and file structure
structure = {
    "traffic_signal_control": {
        "core": [
            "__init__.py",
            "a_star_priority_queue.py",
            "constants.py",
            "utils.py"
        ],
        "infrastructure": {
            "__init__.py": None,
            "simulator": [
                "__init__.py",
                "base_simulator.py",
                "simple_simulator.py",
                "simulator_factory.py"
            ],
            "environment": [
                "__init__.py",
                "traffic_env.py",
                "state_encoder.py",
                "signal_controller.py"
            ],
            "agent": [
                "__init__.py",
                "base_agent.py",
                "dqn_agent.py",
                "replay_buffer.py"
            ]
        },
        "domain": [
            "__init__.py",
            "reward_calculator.py",
            "safety_manager.py",
            "pedestrian_manager.py",
            "turn_manager.py",
            "traffic_patterns.py",
            "action_space.py"
        ],
        "application": [
            "__init__.py",
            "trainer.py",
            "evaluator.py",
            "scenario_manager.py"
        ],
        "presentation": {
            "__init__.py": None,
            "gui": [
                "__init__.py",
                "main_window.py",
                "widgets.py",
                "styles.py"
            ],
            "visualization": [
                "__init__.py",
                "plotter.py",
                "renderer.py"
            ],
            "output": [
                "__init__.py",
                "metrics_display.py",
                "report_generator.py"
            ]
        },
        "config": [
            "__init__.py",
            "default_config.py",
            "training_config.py",
            "simulation_config.py"
        ],
        "tests": [
            "__init__.py",
            "test_simulator.py",
            "test_agent.py",
            "test_environment.py"
        ],
        "scripts": [
            "train.py",
            "train_with_gui.py",
            "evaluate.py",
            "demo.py"
        ],
        "outputs": {
            "models": {},
            "results": {},
            "logs": {}
        },
        "requirements.txt": None,
        "README.md": None,
        "setup.py": None
    }
}


def create_structure(base_path, structure):
    """Recursively create folder and file structure."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for file_name in content:
                open(os.path.join(path, file_name), "a").close()
        else:
            # Create file if None
            open(path, "a").close()


# Create everything in the current working directory
base_directory = os.getcwd()
create_structure(base_directory, structure)

print(f"✅ Folder structure created successfully in: {base_directory}")

# run_demo.py
from traffic_signal_control.infrastructure.simulator import SimulatorFactory
from traffic_signal_control.infrastructure.environment.traffic_env import TrafficEnv
from traffic_signal_control.infrastructure.agent.dqn_agent import DQNAgent

sim = SimulatorFactory.create('simple', seed=42)
env = TrafficEnv(simulator=sim, config={'max_steps_per_episode': 50})
state = env.reset()
agent = DQNAgent(state_size=env.state_encoder.TOTAL_STATE_SIZE, action_size=11)
for i in range(10):
    action = agent.select_action(state, training=False)
    next_state, reward, done, info = env.step(action)
    print(f"step={i} reward={reward:.2f} queue={info.get('queue_sizes')}")
    state = next_state
    if done:
        break
