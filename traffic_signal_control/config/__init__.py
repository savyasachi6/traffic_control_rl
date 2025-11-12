"""
Configuration module: re-export default configs for easy import.
"""

from .default_config import (
    SIMULATOR_CONFIG,
    ENVIRONMENT_CONFIG,
    AGENT_CONFIG,
    TRAINING_CONFIG,
    REWARD_CONFIG,
    SAFETY_CONFIG,
)

__all__ = [
    "default_config",
]
