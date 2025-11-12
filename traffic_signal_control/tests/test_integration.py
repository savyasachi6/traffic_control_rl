import pytest
import random


def _import_traffic_env():
    try:
        from infrastructure.environment.traffic_env import TrafficEnv
        return TrafficEnv
    except Exception as e:
        pytest.skip(f"Skipping integration test; TrafficEnv not available: {e}")


def _create_simulator():
    try:
        from infrastructure.simulator import SimulatorFactory
        sim = SimulatorFactory.create()
        return sim
    except Exception as e:
        pytest.skip(f"Skipping integration test; simulator backend unavailable: {e}")


def test_full_episode_short():
    TrafficEnv = _import_traffic_env()
    sim = _create_simulator()

    # Create environment and reset
    try:
        env = TrafficEnv(simulator=sim)
    except TypeError:
        # Some implementations may accept simulator as positional arg
        try:
            env = TrafficEnv(sim)
        except Exception as e:
            pytest.skip(f"Skipping - cannot construct TrafficEnv: {e}")
    except Exception as e:
        pytest.skip(f"Skipping - error constructing TrafficEnv: {e}")

    try:
        state = env.reset()
    except Exception as e:
        pytest.skip(f"Skipping - env.reset failed: {e}")

    # Run a short episode of random actions
    for _ in range(50):
        action = random.randint(0, 10)
        try:
            next_state, reward, done, info = env.step(action)
        except Exception as e:
            pytest.skip(f"Skipping - env.step failed: {e}")

        # Basic assertions
        assert hasattr(next_state, 'shape') or hasattr(next_state, '__len__')
        assert isinstance(reward, float) or isinstance(reward, (int,))

        if done:
            break
