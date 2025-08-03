"""
Character evolution and progression system for LLMAdventure
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class EvolutionType(Enum):
    """Types of evolution"""
    LEVEL_UP = "level_up"
    SKILL_MASTERY = "skill_mastery"
    CLASS_EVOLUTION = "class_evolution"
    SPECIALIZATION = "specialization"

@dataclass
class EvolutionPath:
    """Evolution path for character development"""
    name: str
    description: str
    requirements: Dict[str, Any]
    benefits: Dict[str, Any]
    unlocked: bool = False

class Evolution:
    """Character evolution and progression system"""
    
    def __init__(self):
        self.evolution_paths = []
        self.specializations = []
        self.mastery_levels = {}
        self.evolution_points = 0
        
    def add_evolution_path(self, path: EvolutionPath):
        """Add evolution path"""
        self.evolution_paths.append(path)
    
    def check_evolution_requirements(self, player_data: Dict[str, Any]) -> List[EvolutionPath]:
        """Check which evolution paths are available"""
        available = []
        
        for path in self.evolution_paths:
            if path.unlocked:
                continue
                
            if self._meets_requirements(path.requirements, player_data):
                available.append(path)
        
        return available
    
    def unlock_evolution_path(self, path_name: str, player_data: Dict[str, Any]) -> bool:
        """Unlock an evolution path"""
        for path in self.evolution_paths:
            if path.name == path_name and not path.unlocked:
                if self._meets_requirements(path.requirements, player_data):
                    path.unlocked = True
                    self._apply_evolution_benefits(path.benefits, player_data)
                    return True
        return False
    
    def _meets_requirements(self, requirements: Dict[str, Any], player_data: Dict[str, Any]) -> bool:
        """Check if player meets evolution requirements"""
        for req_type, req_value in requirements.items():
            if req_type == "level":
                if player_data.get("level", 0) < req_value:
                    return False
            elif req_type == "skill_mastery":
                skill_name, skill_level = req_value
                if player_data.get("skills", {}).get(skill_name, 0) < skill_level:
                    return False
            elif req_type == "reputation":
                if player_data.get("reputation", 0) < req_value:
                    return False
            elif req_type == "quests_completed":
                if len(player_data.get("completed_quests", [])) < req_value:
                    return False
        
        return True
    
    def _apply_evolution_benefits(self, benefits: Dict[str, Any], player_data: Dict[str, Any]):
        """Apply evolution benefits to player"""
        pass
    
    def get_available_evolutions(self, player_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get list of available evolutions"""
        available = self.check_evolution_requirements(player_data)
        
        return [
            {
                "name": path.name,
                "description": path.description,
                "requirements": path.requirements,
                "benefits": path.benefits
            }
            for path in available
        ]
