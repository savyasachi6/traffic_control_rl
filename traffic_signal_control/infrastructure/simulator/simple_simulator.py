"""
Custom Python-based traffic simulator.

Simple but effective simulation of 4-way intersection with:
- Vehicle spawning and movement
- Pedestrian crossing detection
- Emergency vehicle handling
- Turn movement modeling
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Dict, List
from dataclasses import dataclass

from .base_simulator import BaseSimulator


@dataclass
class Vehicle:
	"""Represents a vehicle in the simulation"""
	vehicle_id: str
	approach: str          # N, S, E, W
	distance_m: float
	speed_m_s: float
	movement: str          # straight, left, right
	created_at: int
	committed: bool = False  # In safety zone?


class SimpleTrafficSimulator(BaseSimulator):
	"""
	Simple traffic simulator implementation.

	Features:
	- Stochastic vehicle/pedestrian spawning
	- Physics-based movement
	- Turn movement handling
	- Emergency vehicle support
	- Time-of-day patterns
	"""

	def __init__(self, seed: int = 42, config: Dict = None):
		"""
		Initialize simulator.

		Args:
			seed (int): Random seed
			config (Dict): Configuration overrides
		"""
		super().__init__(seed)

		# Default spawn rates
		self.spawn_rates = {
			'N': 0.5, 'S': 0.5, 'E': 0.5, 'W': 0.5
		}
		self.pedestrian_spawn_rates = {
			'N': 0.2, 'S': 0.2, 'E': 0.2, 'W': 0.2
		}

		# Vehicle tracking
		self.vehicles: Dict[str, Vehicle] = {}  # {vehicle_id: Vehicle}
		self.pedestrians: Dict[str, Dict] = {}  # {ped_id: Pedestrian}
		self.emergency_vehicles: Dict[str, Dict] = {}  # {emerg_id: EmergencyVehicle}

		# Apply config overrides
		if config:
			self.spawn_rates.update(config.get('spawn_rates', {}))
			self.pedestrian_spawn_rates.update(
				config.get('pedestrian_spawn_rates', {})
			)

	def reset(self) -> None:
		"""Reset simulator state"""
		self.vehicles.clear()
		self.pedestrians.clear()
		self.emergency_vehicles.clear()
		self.current_timestep = 0
		self.spawned_count = 0
		self.cleared_count = 0

	def _spawn_vehicles(self) -> List[Dict]:
		"""
		Spawn new vehicles at each approach.

		Returns:
			List of vehicle dictionaries
		"""
		spawned: List[Dict] = []

		for approach in ['N', 'S', 'E', 'W']:
			# Random chance to spawn vehicle
			if np.random.random() < self.spawn_rates[approach]:
				# Random movement (80% straight, 10% left, 10% right)
				rand = np.random.random()
				if rand < 0.8:
					movement = 'straight'
				elif rand < 0.9:
					movement = 'left'
				else:
					movement = 'right'

				# Create vehicle
				vehicle_id = f"V_{self.current_timestep}_{approach}_{len(self.vehicles)}"

				vehicle = Vehicle(
					vehicle_id=vehicle_id,
					approach=approach,
					distance_m=float(np.random.uniform(50, 150)),  # 50-150m away
					speed_m_s=float(np.random.normal(10, 2)),      # ~10 m/s
					movement=movement,
					created_at=self.current_timestep
				)

				self.vehicles[vehicle_id] = vehicle
				self.spawned_count += 1
				spawned.append(self._vehicle_to_dict(vehicle))

		return spawned

	def _update_positions(self, signal_state: Dict[str, str], dt: float) -> None:
		"""
		Update vehicle positions based on signal state.

		Logic:
		- Green signal: vehicles move forward
		- Red/Orange: vehicles slow down/stop
		- Committed zone: vehicles continue through (safety)

		Args:
			signal_state (Dict[str, str]): Current signal states
			dt (float): Time delta
		"""
		for vehicle_id, vehicle in list(self.vehicles.items()):
			approach = vehicle.approach
			signal = signal_state.get(approach, 'red')

			# Determine acceleration based on signal
			if signal == 'green':
				# Accelerate towards speed
				accel = 2  # m/s^2
				vehicle.speed_m_s = min(
					vehicle.speed_m_s + accel * dt, 12
				)
			elif signal == 'orange':
				# Moderate deceleration
				decel = 1  # m/s^2
				vehicle.speed_m_s = max(
					vehicle.speed_m_s - decel * dt, 5
				)
			else:  # red
				# Strong deceleration
				decel = 3  # m/s^2
				vehicle.speed_m_s = max(
					vehicle.speed_m_s - decel * dt, 0
				)

			# Update position
			vehicle.distance_m -= vehicle.speed_m_s * dt

			# Check if in committed zone (can't stop)
			if vehicle.distance_m < 5:
				vehicle.committed = True

			# Remove if cleared intersection
			if vehicle.distance_m <= 0:
				del self.vehicles[vehicle_id]
				self.cleared_count += 1

	def _spawn_pedestrians(self) -> List[Dict]:
		"""
		Spawn pedestrians at crosswalks.

		Returns:
			List of pedestrian dictionaries
		"""
		spawned: List[Dict] = []

		for approach in ['N', 'S', 'E', 'W']:
			if np.random.random() < self.pedestrian_spawn_rates[approach]:
				ped_id = f"P_{self.current_timestep}_{approach}"

				pedestrian = {
					'ped_id': ped_id,
					'approach': approach,
					'distance_m': float(np.random.uniform(10, 30)),
					'speed_m_s': 1.2,  # Walking speed
					'in_crosswalk': False,
					'created_at': self.current_timestep
				}

				self.pedestrians[ped_id] = pedestrian
				self.spawned_count += 1
				spawned.append({
					**pedestrian,
					'type': 'pedestrian',
					'object_id': ped_id
				})

		return spawned

	def _spawn_emergency_vehicles(self) -> List[Dict]:
		"""
		Randomly spawn emergency vehicles.

		Returns:
			List of emergency vehicle dictionaries
		"""
		spawned: List[Dict] = []

		if np.random.random() < 0.01:  # 1% chance
			approach = np.random.choice(['N', 'S', 'E', 'W'])
			emerg_id = f"EMG_{self.current_timestep}_{approach}"

			emerg = {
				'emerg_id': emerg_id,
				'approach': approach,
				'distance_m': float(np.random.uniform(80, 120)),
				'speed_m_s': 18.0,  # Siren speed
				'created_at': self.current_timestep
			}

			self.emergency_vehicles[emerg_id] = emerg
			self.spawned_count += 1
			spawned.append({
				**emerg,
				'type': 'emergency',
				'object_id': emerg_id
			})

		return spawned

	def generate_timestep(self, signal_state: Dict[str, str], dt: float = 1.0) -> pd.DataFrame:
		"""
		Generate sensor data for one timestep.

		Steps:
		1. Spawn new vehicles/pedestrians
		2. Update positions based on signal
		3. Compute A* priorities
		4. Create sensor DataFrame
		"""
		df_data: List[Dict] = []

		# 1. SPAWN PHASE
		df_data.extend(self._spawn_vehicles())
		df_data.extend(self._spawn_pedestrians())
		df_data.extend(self._spawn_emergency_vehicles())

		# 2. MOVEMENT PHASE
		self._update_positions(signal_state, dt)

		# 3. ADD VEHICLES TO SENSOR DATA
		for vehicle in self.vehicles.values():
			df_data.append(self._vehicle_to_dict(vehicle))

		# 4. CREATE DATAFRAME
		if df_data:
			df = pd.DataFrame(df_data)
		else:
			df = pd.DataFrame(columns=[
				'timestamp', 'object_id', 'type', 'approach', 'distance_m',
				'speed_m_s', 'movement', 'f_val', 'h_val', 'priority_score',
				'committed', 'in_crosswalk', 'wait_time'
			])

		# Add timestamp
		df['timestamp'] = self.current_timestep

		# Increment timestep
		self.current_timestep += 1

		return df

	def _vehicle_to_dict(self, vehicle: Vehicle) -> Dict:
		"""Convert vehicle to dictionary for DataFrame"""
		# Compute A* values (will be overridden by priority queue)
		f_val = vehicle.distance_m
		h_val = vehicle.distance_m / max(vehicle.speed_m_s, 0.01)

		return {
			'object_id': vehicle.vehicle_id,
			'type': 'vehicle',
			'approach': vehicle.approach,
			'distance_m': max(0.0, vehicle.distance_m),
			'speed_m_s': max(0.0, vehicle.speed_m_s),
			'lane': 0,
			'movement': vehicle.movement,
			'f_val': f_val,
			'h_val': h_val,
			'priority_score': f_val + h_val,  # Temporary, will be updated
			'committed': vehicle.committed,
			'in_crosswalk': False,
			'wait_time': (self.current_timestep - vehicle.created_at)
		}

	def get_stats(self) -> Dict:
		"""Return simulation statistics"""
		return {
			'spawned_count': self.spawned_count,
			'cleared_count': self.cleared_count,
			'current_vehicles': len(self.vehicles),
			'current_pedestrians': len(self.pedestrians),
			'current_emergencies': len(self.emergency_vehicles),
			'total_current_objects': (
				len(self.vehicles) + 
				len(self.pedestrians) + 
				len(self.emergency_vehicles)
			)
		}
