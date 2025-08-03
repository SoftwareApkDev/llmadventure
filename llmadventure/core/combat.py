"""
Combat system for LLMAdventure
"""

import random
from typing import Optional, Dict, Any
from enum import Enum

from .player import Player
from .creature import Creature
from ..utils.config import Config
from ..utils.logger import logger


class CombatState(Enum):
    """Combat states"""
    INACTIVE = "inactive"
    ACTIVE = "active"
    PLAYER_TURN = "player_turn"
    CREATURE_TURN = "creature_turn"
    FINISHED = "finished"


class Combat:
    """Combat system for managing battles"""
    
    def __init__(self, config: Config):
        self.config = config
        self.state = CombatState.INACTIVE
        self.player = None
        self.creature = None
        self.round = 0
        self.combat_log = []
        
    def start_combat(self, player: Player, creature: Creature):
        """Start a combat encounter"""
        self.player = player
        self.creature = creature
        self.state = CombatState.ACTIVE
        self.round = 1
        self.combat_log = []

        self.player.state = "in_combat"
        self.player.combat_target = creature
        
        logger.combat_event("Combat started", {
            "player": player.name,
            "creature": creature.name,
            "player_health": player.stats.health,
            "creature_health": creature.stats.health
        })
    
    def is_active(self) -> bool:
        """Check if combat is active"""
        return self.state == CombatState.ACTIVE
    
    async def process_round(self):
        """Process one round of combat"""
        if not self.is_active():
            return
        
        try:
            await self._player_turn()

            if not self._check_combat_end():
                await self._creature_turn()
                self._check_combat_end()
            
            self.round += 1
            
        except Exception as e:
            logger.error(f"Error processing combat round: {e}")
            self.state = CombatState.FINISHED
    
    async def _player_turn(self):
        """Process player's turn"""
        if not self.player.is_alive() or not self.creature.is_alive():
            return

        player_damage = self._calculate_player_damage()

        creature_died = self.creature.take_damage(player_damage)

        action_log = {
            "round": self.round,
            "attacker": self.player.name,
            "target": self.creature.name,
            "damage": player_damage,
            "target_health_remaining": self.creature.stats.health,
            "target_died": creature_died
        }
        
        self.combat_log.append(action_log)
        
        logger.combat_event("Player attack", action_log)
    
    async def _creature_turn(self):
        """Process creature's turn"""
        if not self.creature.is_alive() or not self.player.is_alive():
            return

        if self.creature.state.value == "fleeing":
            self._handle_creature_flee()
            return

        creature_damage = self._calculate_creature_damage()

        player_died = self.player.take_damage(creature_damage)

        action_log = {
            "round": self.round,
            "attacker": self.creature.name,
            "target": self.player.name,
            "damage": creature_damage,
            "target_health_remaining": self.player.stats.health,
            "target_died": player_died
        }
        
        self.combat_log.append(action_log)
        
        logger.combat_event("Creature attack", action_log)
    
    def _calculate_player_damage(self) -> int:
        """Calculate player's attack damage"""
        base_damage = self.player.stats.attack

        if self.player.equipped.get("weapon"):
            weapon = self.player.equipped["weapon"]
            base_damage += weapon.get("attack_bonus", 0)

        if self.player.player_class.value == "warrior":
            base_damage += self.player.skills.sword_mastery
        elif self.player.player_class.value == "mage":
            base_damage += self.player.skills.magic_mastery

        variance = random.randint(-2, 2)
        final_damage = max(1, base_damage + variance)
        
        return final_damage
    
    def _calculate_creature_damage(self) -> int:
        """Calculate creature's attack damage"""
        base_damage = self.creature.get_attack_damage()

        variance = random.randint(-1, 1)
        final_damage = max(1, base_damage + variance)
        
        return final_damage
    
    def _check_combat_end(self) -> bool:
        """Check if combat should end"""
        if not self.player.is_alive():
            self._end_combat("player_death")
            return True
        elif not self.creature.is_alive():
            self._end_combat("creature_death")
            return True
        elif self.creature.state.value == "fleeing":
            self._end_combat("creature_flee")
            return True
        
        return False
    
    def _handle_creature_flee(self):
        """Handle creature fleeing"""
        action_log = {
            "round": self.round,
            "creature": self.creature.name,
            "action": "flee",
            "success": True
        }
        
        self.combat_log.append(action_log)
        logger.combat_event("Creature fled", action_log)
    
    def _end_combat(self, reason: str):
        """End combat"""
        self.state = CombatState.FINISHED

        if self.player:
            self.player.state = "exploring"
            self.player.combat_target = None

        combat_summary = {
            "reason": reason,
            "rounds": self.round,
            "player_health": self.player.stats.health if self.player else 0,
            "creature_health": self.creature.stats.health if self.creature else 0,
            "total_actions": len(self.combat_log)
        }
        
        logger.combat_event("Combat ended", combat_summary)
    
    def get_combat_status(self) -> Dict[str, Any]:
        """Get current combat status"""
        if not self.is_active():
            return {"state": "inactive"}
        
        return {
            "state": self.state.value,
            "round": self.round,
            "player": {
                "name": self.player.name,
                "health": self.player.stats.health,
                "max_health": self.player.stats.max_health,
                "health_percentage": self.player.get_health_percentage()
            },
            "creature": {
                "name": self.creature.name,
                "health": self.creature.stats.health,
                "max_health": self.creature.stats.max_health,
                "health_percentage": self.creature.get_health_percentage(),
                "state": self.creature.state.value
            },
            "recent_actions": self.combat_log[-3:] if self.combat_log else []
        }
    
    def get_combat_log(self) -> list:
        """Get full combat log"""
        return self.combat_log.copy()
