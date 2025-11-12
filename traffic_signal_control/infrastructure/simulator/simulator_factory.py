"""
Factory for creating simulator instances
"""

from typing import Dict, Optional, Type
from traffic_signal_control.infrastructure.simulator.base_simulator import BaseSimulator
from traffic_signal_control.infrastructure.simulator.simple_simulator import SimpleTrafficSimulator


class SimulatorFactory:
    """Factory pattern for simulator creation"""
    
    _simulators: Dict[str, Type[BaseSimulator]] = {
        'simple': SimpleTrafficSimulator
    }
    
    @classmethod
    def create(cls, backend: str = 'simple', **kwargs) -> BaseSimulator:
        """Create simulator instance"""
        if backend not in cls._simulators:
            raise ValueError(
                f"Unknown backend: {backend}. Available: {list(cls._simulators.keys())}"
            )
        return cls._simulators[backend](**kwargs)
    
    @classmethod
    def register(cls, name: str, simulator_class: Type[BaseSimulator]) -> None:
        """Register new simulator class"""
        if not issubclass(simulator_class, BaseSimulator):
            raise TypeError(f"{simulator_class} must inherit from BaseSimulator")
        cls._simulators[name] = simulator_class
    
    @classmethod
    def list_backends(cls) -> list:
        """List available backends"""
        return list(cls._simulators.keys())
