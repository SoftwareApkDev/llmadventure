"""
Player character management for LLMAdventure
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import random

class PlayerClass(Enum):
    """Available player classes"""
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    RANGER = "ranger"

class PlayerState(Enum):
    """Player states"""
    EXPLORING = "exploring"
    IN_COMBAT = "in_combat"
    IN_DIALOGUE = "in_dialogue"
    MENU = "menu"

@dataclass
class PlayerStats:
    """Player statistics"""
    health: int = 100
    max_health: int = 100
    mana: int = 50
    max_mana: int = 50
    attack: int = 10
    defense: int = 5
    speed: int = 8
    intelligence: int = 6
    charisma: int = 5
    luck: int = 5

@dataclass
class PlayerSkills:
    """Player skills and abilities"""
    sword_mastery: int = 1
    magic_mastery: int = 1
    stealth: int = 1
    archery: int = 1
    healing: int = 1
    persuasion: int = 1

class Player:
    """Player character class"""
    
    def __init__(self, name: str, player_class: PlayerClass = PlayerClass.WARRIOR):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.experience = 0
        self.experience_to_next = 100

        self.stats = self._get_class_stats(player_class)
        self.skills = PlayerSkills()
        self._apply_class_bonuses()

        self.state = PlayerState.EXPLORING
        self.location = (0, 0)
        self.gold = 50
        self.reputation = 0

        self.inventory = []
        self.equipped = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }

        self.active_quests = []
        self.completed_quests = []

        self.in_combat = False
        self.combat_target = None
        
    def _get_class_stats(self, player_class: PlayerClass) -> PlayerStats:
        """Get base stats for player class"""
        base_stats = PlayerStats()
        
        if player_class == PlayerClass.WARRIOR:
            base_stats.health = 120
            base_stats.max_health = 120
            base_stats.attack = 15
            base_stats.defense = 8
            base_stats.speed = 6
        elif player_class == PlayerClass.MAGE:
            base_stats.mana = 100
            base_stats.max_mana = 100
            base_stats.intelligence = 12
            base_stats.attack = 8
            base_stats.defense = 3
        elif player_class == PlayerClass.ROGUE:
            base_stats.speed = 12
            base_stats.attack = 12
            base_stats.defense = 4
            base_stats.health = 90
            base_stats.max_health = 90
        elif player_class == PlayerClass.RANGER:
            base_stats.speed = 10
            base_stats.attack = 11
            base_stats.defense = 6
            base_stats.health = 100
            base_stats.max_health = 100
            
        return base_stats
    
    def _apply_class_bonuses(self):
        """Apply class-specific skill bonuses"""
        if self.player_class == PlayerClass.WARRIOR:
            self.skills.sword_mastery = 3
        elif self.player_class == PlayerClass.MAGE:
            self.skills.magic_mastery = 3
        elif self.player_class == PlayerClass.ROGUE:
            self.skills.stealth = 3
        elif self.player_class == PlayerClass.RANGER:
            self.skills.archery = 3
    
    def gain_experience(self, amount: int):
        """Gain experience and check for level up"""
        self.experience += amount
        
        while self.experience >= self.experience_to_next:
            self.level_up()
    
    def level_up(self):
        """Level up the player"""
        self.experience -= self.experience_to_next
        self.level += 1
        self.experience_to_next = int(self.experience_to_next * 1.5)

        self.stats.max_health += 10
        self.stats.health = self.stats.max_health
        self.stats.max_mana += 5
        self.stats.mana = self.stats.max_mana
        self.stats.attack += 2
        self.stats.defense += 1
        self.stats.speed += 1
        self.stats.intelligence += 1

        if self.player_class == PlayerClass.WARRIOR:
            self.stats.max_health += 5
            self.stats.attack += 1
        elif self.player_class == PlayerClass.MAGE:
            self.stats.max_mana += 10
            self.stats.intelligence += 2
        elif self.player_class == PlayerClass.ROGUE:
            self.stats.speed += 2
            self.stats.attack += 1
        elif self.player_class == PlayerClass.RANGER:
            self.stats.speed += 1
            self.stats.attack += 1
    
    def take_damage(self, damage: int) -> bool:
        """Take damage and return True if player dies"""
        actual_damage = max(1, damage - self.stats.defense)
        self.stats.health = max(0, self.stats.health - actual_damage)
        return self.stats.health <= 0
    
    def heal(self, amount: int):
        """Heal the player"""
        self.stats.health = min(self.stats.max_health, self.stats.health + amount)
    
    def restore_mana(self, amount: int):
        """Restore mana"""
        self.stats.mana = min(self.stats.max_mana, self.stats.mana + amount)
    
    def is_alive(self) -> bool:
        """Check if player is alive"""
        return self.stats.health > 0
    
    def get_health_percentage(self) -> float:
        """Get health as percentage"""
        return (self.stats.health / self.stats.max_health) * 100
    
    def get_mana_percentage(self) -> float:
        """Get mana as percentage"""
        return (self.stats.mana / self.stats.max_mana) * 100
    
    def move_to(self, x: int, y: int):
        """Move player to new location"""
        self.location = (x, y)
    
    def add_gold(self, amount: int):
        """Add gold to player"""
        self.gold += amount
    
    def spend_gold(self, amount: int) -> bool:
        """Spend gold, return True if successful"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def add_reputation(self, amount: int):
        """Add reputation points"""
        self.reputation += amount
    
    def get_status_effects(self) -> List[str]:
        """Get current status effects"""
        effects = []
        if self.stats.health < self.stats.max_health * 0.25:
            effects.append("Critical Health")
        if self.stats.mana < self.stats.max_mana * 0.25:
            effects.append("Low Mana")
        return effects
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert player to dictionary for saving"""
        return {
            "name": self.name,
            "player_class": self.player_class.value,
            "level": self.level,
            "experience": self.experience,
            "experience_to_next": self.experience_to_next,
            "stats": {
                "health": self.stats.health,
                "max_health": self.stats.max_health,
                "mana": self.stats.mana,
                "max_mana": self.stats.max_mana,
                "attack": self.stats.attack,
                "defense": self.stats.defense,
                "speed": self.stats.speed,
                "intelligence": self.stats.intelligence,
                "charisma": self.stats.charisma,
                "luck": self.stats.luck,
            },
            "skills": {
                "sword_mastery": self.skills.sword_mastery,
                "magic_mastery": self.skills.magic_mastery,
                "stealth": self.skills.stealth,
                "archery": self.skills.archery,
                "healing": self.skills.healing,
                "persuasion": self.skills.persuasion,
            },
            "location": self.location,
            "gold": self.gold,
            "reputation": self.reputation,
            "inventory": self.inventory,
            "equipped": self.equipped,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """Create player from dictionary"""
        player = cls(data["name"], PlayerClass(data["player_class"]))
        player.level = data["level"]
        player.experience = data["experience"]
        player.experience_to_next = data["experience_to_next"]

        stats_data = data["stats"]
        player.stats.health = stats_data["health"]
        player.stats.max_health = stats_data["max_health"]
        player.stats.mana = stats_data["mana"]
        player.stats.max_mana = stats_data["max_mana"]
        player.stats.attack = stats_data["attack"]
        player.stats.defense = stats_data["defense"]
        player.stats.speed = stats_data["speed"]
        player.stats.intelligence = stats_data["intelligence"]
        player.stats.charisma = stats_data["charisma"]
        player.stats.luck = stats_data["luck"]

        skills_data = data["skills"]
        player.skills.sword_mastery = skills_data["sword_mastery"]
        player.skills.magic_mastery = skills_data["magic_mastery"]
        player.skills.stealth = skills_data["stealth"]
        player.skills.archery = skills_data["archery"]
        player.skills.healing = skills_data["healing"]
        player.skills.persuasion = skills_data["persuasion"]

        player.location = tuple(data["location"])
        player.gold = data["gold"]
        player.reputation = data["reputation"]
        player.inventory = data["inventory"]
        player.equipped = data["equipped"]
        player.active_quests = data["active_quests"]
        player.completed_quests = data["completed_quests"]
        
        return player
