from typing import List, Dict, Tuple


class ScenarioManager:
    """Manages test scenarios"""
    
    def __init__(self) -> None:
        self.scenarios: List[Tuple[str, Dict]] = []
    
    def add_scenario(self, scenario_type: str, params: Dict) -> None:
        """Add scenario"""
        self.scenarios.append((scenario_type, params))
    
    def get_scenarios(self) -> List[Tuple[str, Dict]]:
        """Get all scenarios"""
        return self.scenarios.copy()
    
    def clear_scenarios(self) -> None:
        """Clear all scenarios"""
        self.scenarios.clear()
