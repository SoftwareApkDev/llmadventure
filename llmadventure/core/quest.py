"""
Quest system for LLMAdventure
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class QuestType(Enum):
    """Types of quests"""
    KILL = "kill"
    COLLECT = "collect"
    EXPLORE = "explore"
    DELIVER = "deliver"
    ESCORT = "escort"

class QuestStatus(Enum):
    """Quest status"""
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class QuestObjective:
    """Quest objective"""
    description: str
    target: str
    current: int = 0
    required: int = 1
    completed: bool = False

class Quest:
    """Quest class for managing quests"""
    
    def __init__(self, quest_id: str, title: str, description: str, quest_type: QuestType):
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.quest_type = quest_type
        self.status = QuestStatus.AVAILABLE
        self.objectives = []
        self.rewards = {}
        self.level_requirement = 1
        self.reputation_requirement = 0
        
    def add_objective(self, description: str, target: str, required: int = 1):
        """Add objective to quest"""
        objective = QuestObjective(description, target, required=required)
        self.objectives.append(objective)
    
    def update_progress(self, target: str, amount: int = 1):
        """Update quest progress"""
        for objective in self.objectives:
            if objective.target.lower() == target.lower():
                objective.current += amount
                if objective.current >= objective.required:
                    objective.completed = True
                break

        if all(obj.completed for obj in self.objectives):
            self.status = QuestStatus.COMPLETED
    
    def get_progress(self) -> Dict[str, Any]:
        """Get quest progress"""
        return {
            "quest_id": self.quest_id,
            "title": self.title,
            "status": self.status.value,
            "objectives": [
                {
                    "description": obj.description,
                    "current": obj.current,
                    "required": obj.required,
                    "completed": obj.completed
                }
                for obj in self.objectives
            ],
            "completed_count": sum(1 for obj in self.objectives if obj.completed),
            "total_objectives": len(self.objectives)
        }
    
    def can_accept(self, player_level: int, player_reputation: int) -> bool:
        """Check if player can accept quest"""
        return (player_level >= self.level_requirement and 
                player_reputation >= self.reputation_requirement)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quest to dictionary"""
        return {
            "quest_id": self.quest_id,
            "title": self.title,
            "description": self.description,
            "quest_type": self.quest_type.value,
            "status": self.status.value,
            "objectives": [
                {
                    "description": obj.description,
                    "target": obj.target,
                    "current": obj.current,
                    "required": obj.required,
                    "completed": obj.completed
                }
                for obj in self.objectives
            ],
            "rewards": self.rewards,
            "level_requirement": self.level_requirement,
            "reputation_requirement": self.reputation_requirement
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quest':
        """Create quest from dictionary"""
        quest = cls(
            data["quest_id"],
            data["title"],
            data["description"],
            QuestType(data["quest_type"])
        )
        
        quest.status = QuestStatus(data["status"])
        quest.rewards = data.get("rewards", {})
        quest.level_requirement = data.get("level_requirement", 1)
        quest.reputation_requirement = data.get("reputation_requirement", 0)

        for obj_data in data.get("objectives", []):
            objective = QuestObjective(
                description=obj_data["description"],
                target=obj_data["target"],
                current=obj_data.get("current", 0),
                required=obj_data.get("required", 1),
                completed=obj_data.get("completed", False)
            )
            quest.objectives.append(objective)
        
        return quest
