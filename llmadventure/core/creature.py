"""
Creature management for LLMAdventure
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random


class CreatureType(Enum):
    """Types of creatures"""
    HUMANOID = "humanoid"
    BEAST = "beast"
    UNDEAD = "undead"
    DEMON = "demon"
    DRAGON = "dragon"
    ELEMENTAL = "elemental"
    CONSTRUCT = "construct"


class CreatureState(Enum):
    """Creature states"""
    IDLE = "idle"
    HOSTILE = "hostile"
    FLEEING = "fleeing"
    DEAD = "dead"

@dataclass
class CreatureStats:
    """Creature statistics"""
    health: int = 50
    max_health: int = 50
    attack: int = 8
    defense: int = 3
    speed: int = 6
    intelligence: int = 4
    charisma: int = 3
    luck: int = 3

@dataclass
class CreatureAbilities:
    """Creature special abilities"""
    can_fly: bool = False
    can_swim: bool = False
    can_burrow: bool = False
    is_magical: bool = False
    is_undead: bool = False
    is_poisonous: bool = False
    can_regenerate: bool = False


class Creature:
    """Creature class for NPCs and enemies"""
    
    def __init__(self, name: str, creature_type: CreatureType = CreatureType.HUMANOID):
        self.name = name
        self.creature_type = creature_type
        self.level = 1
        self.stats = self._get_base_stats(creature_type)
        self.abilities = self._get_base_abilities(creature_type)
        self.state = CreatureState.IDLE

        self.aggression = 0.3
        self.fear_threshold = 0.2
        self.loot_table = []
        self.experience_value = 10

        self.behavior_pattern = "standard"
        self.dialogue_options = []
        self.quest_related = False

        self.location = (0, 0)
        self.home_location = (0, 0)
        self.wander_radius = 3
        
    def _get_base_stats(self, creature_type: CreatureType) -> CreatureStats:
        """Get base stats for creature type"""
        if creature_type == CreatureType.HUMANOID:
            return CreatureStats(health=60, max_health=60, attack=10, defense=5, speed=7, intelligence=8, charisma=6)
        elif creature_type == CreatureType.BEAST:
            return CreatureStats(health=80, max_health=80, attack=12, defense=4, speed=10, intelligence=3, charisma=2)
        elif creature_type == CreatureType.UNDEAD:
            return CreatureStats(health=70, max_health=70, attack=11, defense=6, speed=5, intelligence=5, charisma=1)
        elif creature_type == CreatureType.DEMON:
            return CreatureStats(health=100, max_health=100, attack=15, defense=7, speed=8, intelligence=10, charisma=8)
        elif creature_type == CreatureType.DRAGON:
            return CreatureStats(health=200, max_health=200, attack=25, defense=15, speed=12, intelligence=15, charisma=12)
        elif creature_type == CreatureType.ELEMENTAL:
            return CreatureStats(health=90, max_health=90, attack=13, defense=8, speed=9, intelligence=7, charisma=4)
        elif creature_type == CreatureType.CONSTRUCT:
            return CreatureStats(health=120, max_health=120, attack=14, defense=12, speed=4, intelligence=6, charisma=1)
        else:
            return CreatureStats()
    
    def _get_base_abilities(self, creature_type: CreatureType) -> CreatureAbilities:
        """Get base abilities for creature type"""
        abilities = CreatureAbilities()
        
        if creature_type == CreatureType.DRAGON:
            abilities.can_fly = True
            abilities.is_magical = True
        elif creature_type == CreatureType.BEAST:
            abilities.can_swim = random.choice([True, False])
        elif creature_type == CreatureType.UNDEAD:
            abilities.is_undead = True
            abilities.can_regenerate = random.choice([True, False])
        elif creature_type == CreatureType.DEMON:
            abilities.is_magical = True
            abilities.can_fly = random.choice([True, False])
        elif creature_type == CreatureType.ELEMENTAL:
            abilities.is_magical = True
            abilities.can_regenerate = True
        elif creature_type == CreatureType.CONSTRUCT:
            abilities.can_regenerate = random.choice([True, False])
            
        return abilities
    
    def take_damage(self, damage: int) -> bool:
        """Take damage and return True if creature dies"""
        actual_damage = max(1, damage - self.stats.defense)
        self.stats.health = max(0, self.stats.health - actual_damage)

        if self.stats.health <= 0:
            self.state = CreatureState.DEAD
            return True
        elif self.stats.health < self.stats.max_health * self.fear_threshold:
            self.state = CreatureState.FLEEING
        elif self.state == CreatureState.IDLE:
            self.state = CreatureState.HOSTILE
            
        return False
    
    def heal(self, amount: int):
        """Heal the creature"""
        self.stats.health = min(self.stats.max_health, self.stats.health + amount)

        if self.stats.health > self.stats.max_health * self.fear_threshold:
            if self.state == CreatureState.FLEEING:
                self.state = CreatureState.IDLE
    
    def is_alive(self) -> bool:
        """Check if creature is alive"""
        return self.stats.health > 0
    
    def get_health_percentage(self) -> float:
        """Get health as percentage"""
        return (self.stats.health / self.stats.max_health) * 100
    
    def should_attack(self, player_level: int, player_reputation: int) -> bool:
        """Determine if creature should attack player"""
        if self.state == CreatureState.DEAD:
            return False
        if self.state == CreatureState.FLEEING:
            return False

        if random.random() < self.aggression:
            return True

        level_diff = self.level - player_level
        if level_diff > 3:
            return random.random() < 0.8
        elif level_diff < -3:
            return random.random() < 0.2

        if player_reputation < -50:
            return random.random() < 0.7
        elif player_reputation > 50:
            return random.random() < 0.3
            
        return False
    
    def get_attack_damage(self) -> int:
        """Calculate attack damage"""
        base_damage = self.stats.attack
        variance = random.randint(-2, 2)
        return max(1, base_damage + variance)
    
    def get_defense_bonus(self) -> int:
        """Calculate defense bonus"""
        return self.stats.defense
    
    def move_to(self, x: int, y: int):
        """Move creature to new location"""
        self.location = (x, y)
    
    def get_loot(self) -> List[Dict[str, Any]]:
        """Get loot from creature"""
        if not self.is_alive():
            return []
            
        loot = []
        for item in self.loot_table:
            if random.random() < item.get("chance", 1.0):
                loot.append(item.copy())
                
        return loot
    
    def get_experience_value(self) -> int:
        """Get experience value for defeating creature"""
        return self.experience_value
    
    def set_level(self, level: int):
        """Set creature level and scale stats"""
        self.level = level
        level_multiplier = 1 + (level - 1) * 0.2
        
        self.stats.max_health = int(self.stats.max_health * level_multiplier)
        self.stats.health = self.stats.max_health
        self.stats.attack = int(self.stats.attack * level_multiplier)
        self.stats.defense = int(self.stats.defense * level_multiplier)
        self.stats.speed = int(self.stats.speed * level_multiplier)
        
        self.experience_value = int(self.experience_value * level_multiplier)
    
    def add_loot_item(self, item: Dict[str, Any], chance: float = 1.0):
        """Add item to loot table"""
        self.loot_table.append({
            "item": item,
            "chance": chance
        })
    
    def set_behavior(self, pattern: str, aggression: float = None, fear_threshold: float = None):
        """Set creature behavior pattern"""
        self.behavior_pattern = pattern
        
        if aggression is not None:
            self.aggression = max(0.0, min(1.0, aggression))
        if fear_threshold is not None:
            self.fear_threshold = max(0.0, min(1.0, fear_threshold))
    
    def add_dialogue_option(self, text: str, conditions: Dict[str, Any] = None):
        """Add dialogue option for creature"""
        self.dialogue_options.append({
            "text": text,
            "conditions": conditions or {}
        })
    
    def get_dialogue_options(self, player_data: Dict[str, Any]) -> List[str]:
        """Get available dialogue options based on player state"""
        options = []
        for option in self.dialogue_options:
            if self._check_dialogue_conditions(option["conditions"], player_data):
                options.append(option["text"])
        return options
    
    def _check_dialogue_conditions(self, conditions: Dict[str, Any], player_data: Dict[str, Any]) -> bool:
        """Check if dialogue conditions are met"""
        for key, value in conditions.items():
            if key not in player_data:
                return False
            if player_data[key] != value:
                return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert creature to dictionary"""
        return {
            "name": self.name,
            "creature_type": self.creature_type.value,
            "level": self.level,
            "stats": {
                "health": self.stats.health,
                "max_health": self.stats.max_health,
                "attack": self.stats.attack,
                "defense": self.stats.defense,
                "speed": self.stats.speed,
                "intelligence": self.stats.intelligence,
                "charisma": self.stats.charisma,
                "luck": self.stats.luck,
            },
            "abilities": {
                "can_fly": self.abilities.can_fly,
                "can_swim": self.abilities.can_swim,
                "can_burrow": self.abilities.can_burrow,
                "is_magical": self.abilities.is_magical,
                "is_undead": self.abilities.is_undead,
                "is_poisonous": self.abilities.is_poisonous,
                "can_regenerate": self.abilities.can_regenerate,
            },
            "state": self.state.value,
            "aggression": self.aggression,
            "fear_threshold": self.fear_threshold,
            "loot_table": self.loot_table,
            "experience_value": self.experience_value,
            "behavior_pattern": self.behavior_pattern,
            "dialogue_options": self.dialogue_options,
            "quest_related": self.quest_related,
            "location": self.location,
            "home_location": self.home_location,
            "wander_radius": self.wander_radius,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Creature':
        """Create creature from dictionary"""
        creature = cls(data["name"], CreatureType(data["creature_type"]))
        creature.level = data["level"]

        stats_data = data["stats"]
        creature.stats.health = stats_data["health"]
        creature.stats.max_health = stats_data["max_health"]
        creature.stats.attack = stats_data["attack"]
        creature.stats.defense = stats_data["defense"]
        creature.stats.speed = stats_data["speed"]
        creature.stats.intelligence = stats_data["intelligence"]
        creature.stats.charisma = stats_data["charisma"]
        creature.stats.luck = stats_data["luck"]

        abilities_data = data["abilities"]
        creature.abilities.can_fly = abilities_data["can_fly"]
        creature.abilities.can_swim = abilities_data["can_swim"]
        creature.abilities.can_burrow = abilities_data["can_burrow"]
        creature.abilities.is_magical = abilities_data["is_magical"]
        creature.abilities.is_undead = abilities_data["is_undead"]
        creature.abilities.is_poisonous = abilities_data["is_poisonous"]
        creature.abilities.can_regenerate = abilities_data["can_regenerate"]

        creature.state = CreatureState(data["state"])
        creature.aggression = data["aggression"]
        creature.fear_threshold = data["fear_threshold"]
        creature.loot_table = data["loot_table"]
        creature.experience_value = data["experience_value"]
        creature.behavior_pattern = data["behavior_pattern"]
        creature.dialogue_options = data["dialogue_options"]
        creature.quest_related = data["quest_related"]
        creature.location = tuple(data["location"])
        creature.home_location = tuple(data["home_location"])
        creature.wander_radius = data["wander_radius"]
        
        return creature
