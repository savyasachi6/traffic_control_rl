"""
Custom Python-based traffic simulator.
Simulates vehicles, pedestrians, and emergencies at 4-way intersection.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from traffic_signal_control.infrastructure.simulator.base_simulator import BaseSimulator
from traffic_signal_control.core.constants import SignalState, Directions


@dataclass
class Vehicle:
    """Represents a vehicle"""
    vehicle_id: str
    approach: str
    distance_m: float
    speed_m_s: float
    movement: str
    created_at: int
    committed: bool = False
    wait_time: float = field(default=0.0)


class SimpleTrafficSimulator(BaseSimulator):
    """Simple stochastic traffic simulator"""
    
    def __init__(self, seed: int = 42, config: Optional[Dict] = None) -> None:
        super().__init__(seed)
        
        self.spawn_rates: Dict[str, float] = {
            'N': 0.5, 'S': 0.5, 'E': 0.5, 'W': 0.5
        }
        self.pedestrian_spawn_rates: Dict[str, float] = {
            'N': 0.2, 'S': 0.2, 'E': 0.2, 'W': 0.2
        }
        
        self.vehicles: Dict[str, Vehicle] = {}
        self.pedestrians: Dict[str, Vehicle] = {}
        self.emergency_vehicles: Dict[str, Vehicle] = {}
        
        if config:
            self.spawn_rates.update(config.get('spawn_rates', {}))
            self.pedestrian_spawn_rates.update(
                config.get('pedestrian_spawn_rates', {})
            )
    
    def reset(self) -> None:
        """Reset simulator"""
        self.vehicles.clear()
        self.pedestrians.clear()
        self.emergency_vehicles.clear()
        self.current_timestep = 0
        self.spawned_count = 0
        self.cleared_count = 0
    
    def _spawn_vehicles(self) -> List[Dict]:
        """Spawn new vehicles"""
        spawned = []
        
        for approach in Directions.ALL:
            if np.random.random() < self.spawn_rates[approach]:
                rand = np.random.random()
                if rand < 0.8:
                    movement = 'straight'
                elif rand < 0.9:
                    movement = 'left'
                else:
                    movement = 'right'
                
                vehicle_id = f"V_{self.current_timestep}_{approach}_{len(self.vehicles)}"
                vehicle = Vehicle(
                    vehicle_id=vehicle_id,
                    approach=approach,
                    distance_m=float(np.random.uniform(50, 150)),
                    speed_m_s=float(np.random.normal(10, 2)),
                    movement=movement,
                    created_at=self.current_timestep,
                    wait_time=0.0
                )
                
                self.vehicles[vehicle_id] = vehicle
                self.spawned_count += 1
                spawned.append(self._vehicle_to_dict(vehicle))
        
        return spawned
    
    def _update_positions(self, signal_state: Dict[str, str], dt: float) -> None:
        """Update vehicle positions based on signals"""
        for vehicle_id, vehicle in list(self.vehicles.items()):
            approach = vehicle.approach
            signal = signal_state.get(approach, SignalState.RED)
            
            if signal == SignalState.GREEN:
                accel = 2.0
                vehicle.speed_m_s = min(vehicle.speed_m_s + accel * dt, 12.0)
            elif signal == SignalState.ORANGE:
                decel = 1.0
                vehicle.speed_m_s = max(vehicle.speed_m_s - decel * dt, 5.0)
            else:
                decel = 3.0
                vehicle.speed_m_s = max(vehicle.speed_m_s - decel * dt, 0.0)
            
            vehicle.distance_m -= vehicle.speed_m_s * dt
            vehicle.wait_time += dt
            
            if vehicle.distance_m < 5:
                vehicle.committed = True
            
            if vehicle.distance_m <= 0:
                del self.vehicles[vehicle_id]
                self.cleared_count += 1
    
    def generate_timestep(self, signal_state: Dict[str, str], 
                         dt: float = 1.0) -> pd.DataFrame:
        """Generate sensor data for one timestep"""
        df_data: List[Dict] = []
        
        df_data.extend(self._spawn_vehicles())
        self._update_positions(signal_state, dt)
        
        for vehicle in self.vehicles.values():
            df_data.append(self._vehicle_to_dict(vehicle))
        
        if df_data:
            df = pd.DataFrame(df_data)
        else:
            df = pd.DataFrame(columns=[
                'timestamp', 'object_id', 'type', 'approach', 'distance_m',
                'speed_m_s', 'movement', 'f_val', 'h_val', 'priority_score',
                'committed', 'wait_time'
            ])
        
        df['timestamp'] = self.current_timestep
        self.current_timestep += 1
        
        return df
    
    def _vehicle_to_dict(self, vehicle: Vehicle) -> Dict:
        """Convert vehicle to dictionary"""
        distance = max(0.0, vehicle.distance_m)
        speed = max(0.01, vehicle.speed_m_s)
        f_val = distance
        h_val = distance / speed
        
        return {
            'object_id': vehicle.vehicle_id,
            'type': 'vehicle',
            'approach': vehicle.approach,
            'distance_m': distance,
            'speed_m_s': speed,
            'lane': 0,
            'movement': vehicle.movement,
            'f_val': float(f_val),
            'h_val': float(h_val),
            'priority_score': float(f_val + h_val),
            'committed': vehicle.committed,
            'wait_time': float(vehicle.wait_time)
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
