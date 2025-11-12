"""
Central configuration and constants for traffic signal control system.
All hardcoded values defined here for easy modification.
"""


class Directions:
    """Cardinal directions at intersection"""
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    ALL = [NORTH, SOUTH, EAST, WEST]
    
    OPPOSITES = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }
    
    PERPENDICULAR = {
        NORTH: [EAST, WEST],
        SOUTH: [EAST, WEST],
        EAST: [NORTH, SOUTH],
        WEST: [NORTH, SOUTH]
    }


class SignalState:
    """Traffic signal states"""
    GREEN = 'green'
    RED = 'red'
    ORANGE = 'orange'
    ALL_RED = 'all_red'
    
    COLORS = {
        GREEN: '#BBFFBB',
        RED: '#FFB6C6',
        ORANGE: '#FFD699',
        ALL_RED: '#404040'
    }
    
    ICONS = {
        GREEN: '🟢',
        RED: '🔴',
        ORANGE: '🟠',
        ALL_RED: '⚫'
    }


class VehicleType:
    """Vehicle classifications"""
    REGULAR = 'vehicle'
    PEDESTRIAN = 'pedestrian'
    EMERGENCY = 'emergency'


class MovementType:
    """Turn movements"""
    STRAIGHT = 'straight'
    LEFT = 'left'
    RIGHT = 'right'


class SimulationConstants:
    """Simulation parameters"""
    BASE_GREEN_TIME = 10
    BASE_ORANGE_TIME = 3
    MIN_GREEN_TIME = 8
    MAX_GREEN_TIME = 60
    MIN_ORANGE_TIME = 3
    
    PEDESTRIAN_CROSSING_SPEED = 1.2
    PEDESTRIAN_CLEARANCE_TIME = 5
    PEDESTRIAN_STARVATION_THRESHOLD = 20
    
    AVERAGE_VEHICLE_SPEED = 10
    VEHICLE_COMMITTED_ZONE = 5
    INTERSECTION_SIZE = 50
    
    DEFAULT_SPAWN_RATE = 0.5
    DEFAULT_PED_SPAWN_RATE = 0.2
    EMERGENCY_SPAWN_RATE = 0.01
    
    PEDESTRIAN_PRIORITY_BIAS = 20
    EMERGENCY_PRIORITY_BIAS = 10000
    LONG_WAIT_BOOST = 10


class ActionSpace:
    """11-action space"""
    NS_GREEN_STRAIGHT = 0
    EW_GREEN_STRAIGHT = 1
    NS_GREEN_WITH_LEFT = 2
    EW_GREEN_WITH_LEFT = 3
    LEFT_TURN_PHASE = 4
    PED_CROSSING = 5
    EXTEND_STRAIGHT = 6
    EXTEND_WITH_TURNS = 7
    RIGHT_ON_RED_NS = 8
    RIGHT_ON_RED_EW = 9
    EMERGENCY_OVERRIDE = 10
    
    TOTAL_ACTIONS = 11
    
    DESCRIPTIONS = {
        0: "N-S Green (straight only)",
        1: "E-W Green (straight only)",
        2: "N-S Green (with left turns)",
        3: "E-W Green (with left turns)",
        4: "Left turn exclusive phase",
        5: "Pedestrian crossing",
        6: "Extend straight traffic",
        7: "Extend with turns",
        8: "Right-on-red N-S",
        9: "Right-on-red E-W",
        10: "Emergency override"
    }


class RewardConstants:
    """Multi-objective reward weights"""
    THROUGHPUT_WEIGHT = 1.0
    FAIRNESS_WEIGHT = 0.5
    SAFETY_WEIGHT = 100.0
    PEDESTRIAN_WEIGHT = 2.0
    EFFICIENCY_WEIGHT = 0.2
    
    RISKY_EVENT_PENALTY = -100.0
    STEP_PENALTY = -0.1
    EXTENSION_PENALTY = -0.2
    
    RUSH_MODE_BONUS = 5.0
    PERFECT_FAIRNESS_BONUS = 10.0
