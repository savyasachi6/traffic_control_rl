"""
Factory Pattern implementation for simulator creation.

Allows easy switching between different simulator backends
without changing client code.
"""

from typing import Dict, Optional, Type

from .base_simulator import BaseSimulator
from .simple_simulator import SimpleTrafficSimulator


class SimulatorFactory:
	"""
	Factory for creating simulator instances.

	Usage:
		sim = SimulatorFactory.create('simple', config={...})
	"""

	_simulators: Dict[str, Type[BaseSimulator]] = {
		'simple': SimpleTrafficSimulator,
		# 'sumo': SUMOSimulator,  # Can add later
	}

	@classmethod
	def create(cls, backend: str = 'simple', **kwargs) -> BaseSimulator:
		"""
		Create simulator instance.

		Args:
			backend (str): Simulator type ('simple', 'sumo', 'hybrid')
			**kwargs: Arguments to pass to simulator

		Returns:
			BaseSimulator: Simulator instance

		Raises:
			ValueError: If backend not supported
		"""
		if backend not in cls._simulators:
			raise ValueError(
				f"Unknown backend: {backend}. "
				f"Supported: {list(cls._simulators.keys())}"
			)

		SimulatorClass = cls._simulators[backend]
		return SimulatorClass(**kwargs)

	@classmethod
	def register(cls, name: str, simulator_class: Type[BaseSimulator]) -> None:
		"""
		Register a new simulator type.

		Allows extending with custom simulators.

		Args:
			name (str): Simulator name
			simulator_class (type): Simulator class
		"""
		cls._simulators[name] = simulator_class

