"""
Main Game class for LLMAdventure
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .player import Player, PlayerClass
from .world import World
from .combat import Combat
from .quest import Quest
from .inventory import Inventory
from ..engine.llm_interface import LLMInterface
from ..engine.procedural_gen import ProceduralGenerator
from ..utils.config import Config
from ..utils.logger import logger


class Game:
    """Main game class that coordinates all game systems"""

    def __init__(self, config: Config):
        self.config = config
        self.player = None
        self.world = None
        self.combat = None
        self.llm = LLMInterface(config)
        self.generator = ProceduralGenerator(config)

        self.game_running = False
        self.current_location = None
        self.creatures_at_location = []
        self.items_at_location = []
        self.quests_available = []

        self.save_file = None
        self.auto_save_enabled = True

    async def initialize_new_game(self, player_name: str, player_class: str):
        """Initialize a new game"""
        try:
            player_class_enum = PlayerClass(player_class)
            self.player = Player(player_name, player_class_enum)

            self.world = World(self.config)
            await self.world.initialize_world()

            self.combat = Combat(self.config)

            self.current_location = self.world.get_location(self.player.location)
            self.player.location = (0, 0)

            await self._generate_location_content()

            if self.auto_save_enabled:
                await asyncio.create_task(self._auto_save_loop())

            self.game_running = True
            logger.game_event("New game started", {
                "player_name": player_name,
                "player_class": player_class,
                "location": self.player.location
            })

        except Exception as e:
            logger.error(f"Error initializing new game: {e}")
            raise

    async def load_game(self, save_file: str):
        """Load a saved game"""
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)

            self.player = Player.from_dict(save_data["player"])

            self.world = World(self.config)
            await self.world.load_from_dict(save_data["world"])

            self.combat = Combat(self.config)

            self.current_location = self.world.get_location(self.player.location)

            await self._generate_location_content()

            if self.auto_save_enabled:
                await asyncio.create_task(self._auto_save_loop())

            self.save_file = save_file
            self.game_running = True

            logger.game_event("Game loaded", {"save_file": save_file})

        except Exception as e:
            logger.error(f"Error loading game: {e}")
            raise

    async def save_game(self, save_name: Optional[str] = None):
        """Save the current game"""
        try:
            if not save_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_name = f"save_{self.player.name}_{timestamp}.json"

            save_dir = Path(self.config.get_data_dir()) / "saves"
            save_dir.mkdir(parents=True, exist_ok=True)

            save_file = save_dir / save_name

            save_data = {
                "version": "0.1.0",
                "timestamp": datetime.now().isoformat(),
                "player": self.player.to_dict(),
                "world": self.world.to_dict(),
                "current_location": self.current_location.to_dict() if self.current_location else None,
            }

            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)

            self.save_file = str(save_file)
            logger.game_event("Game saved", {"save_file": str(save_file)})

        except Exception as e:
            logger.error(f"Error saving game: {e}")
            raise

    async def move_player(self, direction: str):
        """Move player in specified direction"""
        try:
            if not self.game_running:
                return

            x, y = self.player.location

            if direction == "north":
                new_location = (x, y - 1)
            elif direction == "south":
                new_location = (x, y + 1)
            elif direction == "east":
                new_location = (x + 1, y)
            elif direction == "west":
                new_location = (x - 1, y)
            else:
                logger.warning(f"Invalid direction: {direction}")
                return

            if not self.world.has_location(new_location):
                await self.world.generate_location(new_location)

            self.player.move_to(*new_location)
            self.current_location = self.world.get_location(new_location)

            await self._generate_location_content()

            logger.game_event("Player moved", {
                "direction": direction,
                "from": (x, y),
                "to": new_location
            })

        except Exception as e:
            logger.error(f"Error moving player: {e}")
            raise

    async def look_around(self):
        """Generate description of current location"""
        try:
            if not self.current_location:
                return

            player_state = self._get_player_state()
            world_context = self.world.get_context_for_location(self.player.location)

            description = await self.llm.generate_story_segment(
                self.current_location.name,
                player_state,
                world_context
            )

            from ..cli.display import DisplayManager
            display = DisplayManager()
            await display.show_location_description(description, self.current_location)

        except Exception as e:
            logger.error(f"Error looking around: {e}")
            raise

    async def attack_creature(self, creature_name: str):
        """Attack a creature at current location"""
        try:
            if not self.game_running:
                return

            target_creature = None
            for creature in self.creatures_at_location:
                if creature.name.lower() == creature_name.lower():
                    target_creature = creature
                    break

            if not target_creature:
                logger.warning(f"Creature not found: {creature_name}")
                return

            self.combat.start_combat(self.player, target_creature)

            while self.combat.is_active():
                await self.combat.process_round()

                if not self.player.is_alive():
                    await self._handle_player_death()
                    break
                elif not target_creature.is_alive():
                    await self._handle_creature_death(target_creature)
                    break

        except Exception as e:
            logger.error(f"Error in combat: {e}")
            raise

    async def talk_to_npc(self, npc_name: str):
        """Talk to an NPC at current location"""
        try:
            npc = None
            for creature in self.creatures_at_location:
                if (creature.name.lower() == npc_name.lower() and
                        creature.creature_type.value == "humanoid"):
                    npc = creature
                    break

            if not npc:
                logger.warning(f"NPC not found: {npc_name}")
                return

            player_data = self._get_player_state()
            conversation_context = {
                "location": self.current_location.name,
                "time": "day",
                "weather": "clear"
            }

            from ..cli.display import DisplayManager
            display = DisplayManager()

            npc_data = npc.to_dict()
            response = await self.llm.generate_dialogue_response(
                npc_data,
                "Hello",
                conversation_context
            )

            await display.show_dialogue(npc.name, response)

        except Exception as e:
            logger.error(f"Error talking to NPC: {e}")
            raise

    async def use_item(self, item_name: str):
        """Use an item from inventory"""
        try:
            item = None
            for inv_item in self.player.inventory:
                if inv_item["name"].lower() == item_name.lower():
                    item = inv_item
                    break

            if not item:
                logger.warning(f"Item not found in inventory: {item_name}")
                return

            if item["type"] == "consumable":
                if "health" in item["effects"]:
                    self.player.heal(item["effects"]["health"])
                if "mana" in item["effects"]:
                    self.player.restore_mana(item["effects"]["mana"])

                self.player.inventory.remove(item)

                logger.game_event("Item used", {"item": item_name, "effects": item["effects"]})

        except Exception as e:
            logger.error(f"Error using item: {e}")
            raise

    async def take_item(self, item_name: str):
        """Take an item from current location"""
        try:
            item = None
            for loc_item in self.items_at_location:
                if loc_item["name"].lower() == item_name.lower():
                    item = loc_item
                    break

            if not item:
                logger.warning(f"Item not found at location: {item_name}")
                return

            self.player.inventory.append(item)
            self.items_at_location.remove(item)

            logger.game_event("Item taken", {"item": item_name})

        except Exception as e:
            logger.error(f"Error taking item: {e}")
            raise

    async def process_command(self, command: str):
        """Process custom commands"""
        try:
            logger.warning(f"Unknown command: {command}")

        except Exception as e:
            logger.error(f"Error processing command: {e}")
            raise

    async def _generate_location_content(self):
        """Generate creatures and items for current location"""
        try:
            if not self.current_location:
                return

            self.creatures_at_location = await self.generator.generate_creatures_for_location(
                self.current_location,
                self.player.level
            )

            self.items_at_location = await self.generator.generate_items_for_location(
                self.current_location,
                self.player.level
            )

            self.quests_available = await self.generator.generate_quests_for_location(
                self.current_location,
                self.player.level
            )

        except Exception as e:
            logger.error(f"Error generating location content: {e}")
            raise

    async def _handle_player_death(self):
        """Handle player death"""
        try:
            logger.game_event("Player died")

            self.player.location = (0, 0)
            self.player.stats.health = self.player.stats.max_health // 2
            self.player.stats.mana = self.player.stats.max_mana // 2

            self.current_location = self.world.get_location(self.player.location)
            await self._generate_location_content()

        except Exception as e:
            logger.error(f"Error handling player death: {e}")
            raise

    async def _handle_creature_death(self, creature):
        """Handle creature death"""
        try:
            exp_gained = creature.get_experience_value()
            self.player.gain_experience(exp_gained)

            loot = creature.get_loot()
            for item in loot:
                self.player.inventory.append(item["item"])

            self.creatures_at_location.remove(creature)

            logger.combat_event("Creature defeated", {
                "creature": creature.name,
                "exp_gained": exp_gained,
                "loot_count": len(loot)
            })

        except Exception as e:
            logger.error(f"Error handling creature death: {e}")
            raise

    def _get_player_state(self) -> Dict[str, Any]:
        """Get current player state for LLM context"""
        return {
            "name": self.player.name,
            "level": self.player.level,
            "health": self.player.stats.health,
            "max_health": self.player.stats.max_health,
            "mana": self.player.stats.mana,
            "max_mana": self.player.stats.max_mana,
            "gold": self.player.gold,
            "reputation": self.player.reputation,
            "location": self.player.location,
            "class": self.player.player_class.value,
        }

    async def _auto_save_loop(self):
        """Auto-save loop"""
        while self.game_running:
            try:
                await asyncio.sleep(self.config.get("save_interval", 5) * 60)
                if self.game_running:
                    await self.save_game()
            except Exception as e:
                logger.error(f"Error in auto-save: {e}")

    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state"""
        return {
            "player": self._get_player_state(),
            "location": self.current_location.to_dict() if self.current_location else None,
            "creatures": [c.to_dict() for c in self.creatures_at_location],
            "items": self.items_at_location,
            "quests": [q.to_dict() for q in self.quests_available],
            "world_seed": self.world.seed if self.world else None,
        }
