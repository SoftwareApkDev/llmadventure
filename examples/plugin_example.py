#!/usr/bin/env python3
"""
Plugin example for LLMAdventure

This example demonstrates how to create custom plugins
to extend the game's functionality.
"""

import asyncio
from typing import Dict, Any, Optional
from llmadventure.plugins import Plugin, register_plugin
from llmadventure.core.game import Game
from llmadventure.core.player import Player
from llmadventure.core.creature import Creature
from llmadventure.core.quest import Quest


@register_plugin
class CombatEnhancerPlugin(Plugin):
    """Plugin that enhances combat mechanics"""
    
    name = "Combat Enhancer"
    version = "1.0.0"
    description = "Adds special combat abilities and effects"
    
    def __init__(self):
        super().__init__()
        self.combat_bonuses = {}
        self.special_abilities = {}
    
    def on_game_start(self, game: Game):
        """Initialize plugin when game starts"""
        print("⚔️ Combat Enhancer Plugin loaded!")

        self._add_special_abilities(game.player)
    
    def on_combat_start(self, player: Player, enemy: Creature):
        """Called when combat begins"""
        print(f"🔥 Combat Enhancer: {player.name} vs {enemy.name}")

        bonus = self._calculate_combat_bonus(player)
        self.combat_bonuses[player.name] = bonus
        
        print(f"⚡ Combat bonus applied: +{bonus} attack")
    
    def on_combat_turn(self, player: Player, enemy: Creature, turn: int):
        """Called on each combat turn"""
        if turn % 3 == 0:
            self._trigger_special_ability(player, enemy)
    
    def on_combat_end(self, player: Player, enemy: Creature, victory: bool):
        """Called when combat ends"""
        if victory:
            bonus_exp = self._calculate_victory_bonus(enemy)
            player.experience += bonus_exp
            print(f"🏆 Victory bonus: +{bonus_exp} experience")

        self.combat_bonuses.pop(player.name, None)
    
    def _add_special_abilities(self, player: Player):
        """Add special abilities to player"""
        abilities = {
            "warrior": ["Charge Attack", "Defensive Stance"],
            "mage": ["Fireball", "Ice Shield"],
            "rogue": ["Backstab", "Stealth"],
            "ranger": ["Precise Shot", "Animal Companion"]
        }
        
        player_class = player.player_class.value
        if player_class in abilities:
            self.special_abilities[player.name] = abilities[player_class]
            print(f"🎯 Special abilities added: {', '.join(abilities[player_class])}")
    
    def _calculate_combat_bonus(self, player: Player) -> int:
        """Calculate combat bonus based on player stats"""
        base_bonus = player.level * 2
        if player.player_class.value == "warrior":
            base_bonus += 5
        return base_bonus
    
    def _trigger_special_ability(self, player: Player, enemy: Creature):
        """Trigger a special ability"""
        abilities = self.special_abilities.get(player.name, [])
        if abilities:
            ability = abilities[0]
            print(f"✨ {player.name} uses {ability}!")

            if ability == "Charge Attack":
                damage = player.attack * 2
                enemy.health -= damage
                print(f"💥 {enemy.name} takes {damage} damage!")
    
    def _calculate_victory_bonus(self, enemy: Creature) -> int:
        """Calculate bonus experience for victory"""
        return enemy.level * 10


@register_plugin
class QuestGeneratorPlugin(Plugin):
    """Plugin that generates custom quests"""
    
    name = "Quest Generator"
    version = "1.0.0"
    description = "Generates dynamic quests based on player actions"
    
    def __init__(self):
        super().__init__()
        self.quest_templates = [
            {
                "title": "Monster Hunter",
                "description": "Defeat {count} {creature_type} creatures",
                "type": "combat",
                "target_count": 3,
                "reward_exp": 100
            },
            {
                "title": "Explorer",
                "description": "Visit {count} different locations",
                "type": "exploration",
                "target_count": 5,
                "reward_exp": 75
            },
            {
                "title": "Collector",
                "description": "Collect {count} {item_type} items",
                "type": "collection",
                "target_count": 10,
                "reward_exp": 50
            }
        ]
        self.active_quests = {}
    
    def on_game_start(self, game: Game):
        """Initialize plugin when game starts"""
        print("📜 Quest Generator Plugin loaded!")
        self._generate_starter_quest(game.player)
    
    def on_creature_defeated(self, player: Player, creature: Creature):
        """Called when a creature is defeated"""
        self._update_quest_progress(player, "combat")
    
    def on_location_visited(self, player: Player, location: Dict[str, Any]):
        """Called when player visits a new location"""
        self._update_quest_progress(player, "exploration")
    
    def on_item_collected(self, player: Player, item: Dict[str, Any]):
        """Called when player collects an item"""
        self._update_quest_progress(player, "collection")
    
    def _generate_starter_quest(self, player: Player):
        """Generate a starter quest for the player"""
        import random
        
        template = random.choice(self.quest_templates)
        quest = Quest(
            title=template["title"],
            description=template["description"].format(
                count=template["target_count"],
                creature_type="goblin",
                item_type="treasure"
            ),
            quest_type=template["type"],
            target_count=template["target_count"],
            reward_exp=template["reward_exp"]
        )
        
        self.active_quests[player.name] = quest
        print(f"📋 New quest available: {quest.title}")
        print(f"   {quest.description}")
    
    def _update_quest_progress(self, player: Player, quest_type: str):
        """Update quest progress"""
        quest = self.active_quests.get(player.name)
        if quest and quest.quest_type == quest_type:
            quest.progress += 1
            print(f"📈 Quest progress: {quest.progress}/{quest.target_count}")
            
            if quest.progress >= quest.target_count:
                self._complete_quest(player, quest)
    
    def _complete_quest(self, player: Player, quest: Quest):
        """Complete a quest and give rewards"""
        player.experience += quest.reward_exp
        print(f"🎉 Quest completed: {quest.title}")
        print(f"🏆 Reward: +{quest.reward_exp} experience")

        self._generate_starter_quest(player)


@register_plugin
class WeatherPlugin(Plugin):
    """Plugin that adds weather effects to the game"""
    
    name = "Weather System"
    version = "1.0.0"
    description = "Adds dynamic weather that affects gameplay"
    
    def __init__(self):
        super().__init__()
        self.weather_conditions = ["sunny", "rainy", "stormy", "foggy", "windy"]
        self.current_weather = "sunny"
        self.weather_effects = {
            "sunny": {"combat_bonus": 0, "movement_bonus": 0},
            "rainy": {"combat_bonus": -2, "movement_bonus": -1},
            "stormy": {"combat_bonus": -5, "movement_bonus": -3},
            "foggy": {"combat_bonus": -1, "movement_bonus": -2},
            "windy": {"combat_bonus": 1, "movement_bonus": 1}
        }
    
    def on_game_start(self):
        """Initialize plugin when game starts"""
        print("🌤️ Weather System Plugin loaded!")
        self._change_weather()
    
    def on_player_move(self):
        """Called when player moves"""
        import random
        if random.random() < 0.1:
            self._change_weather()
    
    def on_combat_start(self):
        """Called when combat begins"""
        effects = self.weather_effects[self.current_weather]
        if effects["combat_bonus"] != 0:
            print(f"🌤️ Weather effect: {effects['combat_bonus']:+d} combat bonus")
    
    def _change_weather(self):
        """Change the weather condition"""
        import random
        old_weather = self.current_weather
        self.current_weather = random.choice(self.weather_conditions)
        
        if old_weather != self.current_weather:
            print(f"🌤️ Weather changed: {old_weather} → {self.current_weather}")
            
            effects = self.weather_effects[self.current_weather]
            if effects["combat_bonus"] != 0 or effects["movement_bonus"] != 0:
                print(f"   Effects: Combat {effects['combat_bonus']:+d}, Movement {effects['movement_bonus']:+d}")


async def main():
    """Demonstrate plugin functionality"""
    
    print("🔌 LLMAdventure Plugin Examples")
    print("=" * 50)
    
    print("📦 Available Plugins:")
    print("   - Combat Enhancer: Adds special combat abilities")
    print("   - Quest Generator: Creates dynamic quests")
    print("   - Weather System: Adds weather effects")
    
    print("\n🎯 Plugin Features:")
    print("   - Event-driven architecture")
    print("   - Easy to extend and customize")
    print("   - Modular design")
    print("   - Hot-reloadable")
    
    print("\n📚 To use these plugins:")
    print("   1. Install LLMAdventure")
    print("   2. Create your plugin file")
    print("   3. Use the @register_plugin decorator")
    print("   4. Implement event handlers")
    print("   5. Start the game!")
    
    print("\n🎉 Plugin system ready for your creativity!")


if __name__ == "__main__":
    asyncio.run(main())
