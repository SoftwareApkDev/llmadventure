"""
Procedural generation engine for LLMAdventure
"""

import random
from typing import Dict, List, Optional, Any
from ..core.creature import Creature, CreatureType
from ..core.world import Location
from ..core.quest import Quest, QuestType
from ..utils.config import Config
from ..utils.logger import logger

class ProceduralGenerator:
    """Procedural content generation system"""
    
    def __init__(self, config: Config):
        self.config = config
        self.seed = random.randint(1, 1000000)
        
    async def generate_creatures_for_location(self, location: Location, player_level: int) -> List[Creature]:
        """Generate creatures for a location"""
        creatures = []
        
        # Determine number of creatures based on location difficulty
        num_creatures = random.randint(0, min(3, location.difficulty))
        
        for _ in range(num_creatures):
            creature = await self._generate_creature(location, player_level)
            if creature:
                creatures.append(creature)
        
        return creatures
    
    async def generate_items_for_location(self, location: Location, player_level: int) -> List[Dict[str, Any]]:
        """Generate items for a location"""
        items = []
        
        # Determine number of items based on location
        num_items = random.randint(0, 2)
        
        for _ in range(num_items):
            item = self._generate_item(location, player_level)
            if item:
                items.append(item)
        
        return items
    
    async def generate_quests_for_location(self, location: Location, player_level: int) -> List[Quest]:
        """Generate quests for a location"""
        quests = []
        
        # Chance of quest based on location type
        if random.random() < 0.3:  # 30% chance
            quest = self._generate_quest(location, player_level)
            if quest:
                quests.append(quest)
        
        return quests
    
    async def _generate_creature(self, location: Location, player_level: int) -> Optional[Creature]:
        """Generate a single creature"""
        try:
            # Determine creature type based on location
            creature_type = self._get_creature_type_for_location(location)
            
            # Generate creature name
            name = self._generate_creature_name(creature_type)
            
            # Create creature
            creature = Creature(name, creature_type)
            
            # Set level based on location difficulty and player level
            creature_level = max(1, min(10, location.difficulty + random.randint(-1, 1)))
            creature.set_level(creature_level)
            
            # Add loot
            self._add_creature_loot(creature, creature_level)
            
            # Set behavior
            self._set_creature_behavior(creature, location)
            
            return creature
            
        except Exception as e:
            logger.error(f"Error generating creature: {e}")
            return None
    
    def _get_creature_type_for_location(self, location: Location) -> CreatureType:
        """Get appropriate creature type for location"""
        biome_creatures = {
            "forest": [CreatureType.BEAST, CreatureType.HUMANOID],
            "mountain": [CreatureType.BEAST, CreatureType.DRAGON],
            "desert": [CreatureType.BEAST, CreatureType.CONSTRUCT],
            "swamp": [CreatureType.UNDEAD, CreatureType.BEAST],
            "plains": [CreatureType.HUMANOID, CreatureType.BEAST],
            "cave": [CreatureType.UNDEAD, CreatureType.DEMON],
            "ruins": [CreatureType.UNDEAD, CreatureType.CONSTRUCT]
        }
        
        available_types = biome_creatures.get(location.biome, [CreatureType.HUMANOID])
        return random.choice(available_types)
    
    def _generate_creature_name(self, creature_type: CreatureType) -> str:
        """Generate creature name"""
        type_names = {
            CreatureType.HUMANOID: ["Villager", "Merchant", "Guard", "Traveler"],
            CreatureType.BEAST: ["Wolf", "Bear", "Eagle", "Snake"],
            CreatureType.UNDEAD: ["Skeleton", "Zombie", "Ghost", "Wraith"],
            CreatureType.DEMON: ["Imp", "Demon", "Fiend", "Devil"],
            CreatureType.DRAGON: ["Dragon", "Wyvern", "Drake", "Wyrm"],
            CreatureType.ELEMENTAL: ["Fire Elemental", "Water Elemental", "Earth Elemental"],
            CreatureType.CONSTRUCT: ["Golem", "Automaton", "Guardian", "Construct"]
        }
        
        names = type_names.get(creature_type, ["Creature"])
        return random.choice(names)
    
    def _add_creature_loot(self, creature: Creature, level: int):
        """Add loot to creature"""
        # Basic loot based on level
        if random.random() < 0.7:  # 70% chance of gold
            gold_amount = random.randint(level * 2, level * 10)
            creature.add_loot_item({
                "name": "Gold Coins",
                "type": "currency",
                "value": gold_amount
            }, chance=0.7)
        
        # Rare loot based on level
        if random.random() < 0.1:  # 10% chance of rare item
            rare_item = self._generate_rare_item(level)
            if rare_item:
                creature.add_loot_item(rare_item, chance=0.1)
    
    def _set_creature_behavior(self, creature: Creature, location: Location):
        """Set creature behavior based on location"""
        if location.biome == "plains":
            creature.set_behavior("peaceful", aggression=0.1)
        elif location.biome in ["cave", "ruins"]:
            creature.set_behavior("aggressive", aggression=0.8)
        else:
            creature.set_behavior("standard", aggression=0.3)
    
    def _generate_item(self, location: Location, player_level: int) -> Optional[Dict[str, Any]]:
        """Generate a single item"""
        try:
            # Determine item type based on location
            item_type = self._get_item_type_for_location(location)
            
            # Generate item
            if item_type == "weapon":
                return self._generate_weapon(player_level)
            elif item_type == "armor":
                return self._generate_armor(player_level)
            elif item_type == "consumable":
                return self._generate_consumable()
            else:
                return self._generate_material()
                
        except Exception as e:
            logger.error(f"Error generating item: {e}")
            return None
    
    def _get_item_type_for_location(self, location: Location) -> str:
        """Get appropriate item type for location"""
        biome_items = {
            "forest": ["material", "consumable"],
            "mountain": ["weapon", "material"],
            "desert": ["material", "consumable"],
            "swamp": ["consumable", "material"],
            "plains": ["consumable", "material"],
            "cave": ["weapon", "armor"],
            "ruins": ["weapon", "armor"]
        }
        
        available_types = biome_items.get(location.biome, ["material"])
        return random.choice(available_types)
    
    def _generate_weapon(self, player_level: int) -> Dict[str, Any]:
        """Generate a weapon"""
        weapons = [
            {"name": "Iron Sword", "attack_bonus": 3, "value": 50},
            {"name": "Steel Axe", "attack_bonus": 4, "value": 75},
            {"name": "Magic Staff", "attack_bonus": 5, "value": 100},
            {"name": "Enchanted Bow", "attack_bonus": 4, "value": 80}
        ]
        
        weapon = random.choice(weapons).copy()
        weapon["type"] = "weapon"
        weapon["slot"] = "weapon"
        weapon["level_requirement"] = max(1, player_level - 1)
        
        return weapon
    
    def _generate_armor(self, player_level: int) -> Dict[str, Any]:
        """Generate armor"""
        armors = [
            {"name": "Leather Armor", "defense_bonus": 2, "value": 30},
            {"name": "Chain Mail", "defense_bonus": 4, "value": 60},
            {"name": "Plate Armor", "defense_bonus": 6, "value": 90},
            {"name": "Magic Robes", "defense_bonus": 3, "value": 70}
        ]
        
        armor = random.choice(armors).copy()
        armor["type"] = "armor"
        armor["slot"] = "armor"
        armor["level_requirement"] = max(1, player_level - 1)
        
        return armor
    
    def _generate_consumable(self) -> Dict[str, Any]:
        """Generate a consumable item"""
        consumables = [
            {"name": "Health Potion", "effects": {"health": 20}, "value": 15},
            {"name": "Mana Potion", "effects": {"mana": 25}, "value": 20},
            {"name": "Antidote", "effects": {"cure_poison": True}, "value": 25}
        ]
        
        consumable = random.choice(consumables).copy()
        consumable["type"] = "consumable"
        
        return consumable
    
    def _generate_material(self) -> Dict[str, Any]:
        """Generate a material item"""
        materials = [
            {"name": "Iron Ore", "value": 5},
            {"name": "Herbs", "value": 3},
            {"name": "Gemstone", "value": 15},
            {"name": "Ancient Relic", "value": 25}
        ]
        
        material = random.choice(materials).copy()
        material["type"] = "material"
        
        return material
    
    def _generate_rare_item(self, level: int) -> Optional[Dict[str, Any]]:
        """Generate a rare item"""
        rare_items = [
            {"name": "Legendary Sword", "type": "weapon", "attack_bonus": 10, "value": 500},
            {"name": "Dragon Scale Armor", "type": "armor", "defense_bonus": 12, "value": 400},
            {"name": "Phoenix Feather", "type": "material", "value": 200}
        ]
        
        if random.random() < 0.1:  # 10% chance
            return random.choice(rare_items)
        
        return None
    
    def _generate_quest(self, location: Location, player_level: int) -> Optional[Quest]:
        """Generate a quest for the location"""
        try:
            quest_types = [QuestType.KILL, QuestType.COLLECT, QuestType.EXPLORE]
            quest_type = random.choice(quest_types)
            
            quest_id = f"quest_{location.biome}_{random.randint(1, 1000)}"
            title = self._generate_quest_title(quest_type, location)
            description = self._generate_quest_description(quest_type, location)
            
            quest = Quest(quest_id, title, description, quest_type)
            
            # Add objectives based on quest type
            if quest_type == QuestType.KILL:
                target = self._generate_creature_name(self._get_creature_type_for_location(location))
                quest.add_objective(f"Defeat {target}", target, required=random.randint(1, 3))
            elif quest_type == QuestType.COLLECT:
                item = self._generate_material()
                quest.add_objective(f"Collect {item['name']}", item['name'], required=random.randint(1, 5))
            elif quest_type == QuestType.EXPLORE:
                quest.add_objective(f"Explore {location.name}", location.name, required=1)
            
            # Add rewards
            quest.rewards = {
                "experience": random.randint(50, 200),
                "gold": random.randint(20, 100)
            }
            
            quest.level_requirement = max(1, player_level - 2)
            
            return quest
            
        except Exception as e:
            logger.error(f"Error generating quest: {e}")
            return None
    
    def _generate_quest_title(self, quest_type: QuestType, location: Location) -> str:
        """Generate quest title"""
        titles = {
            QuestType.KILL: [f"Clear {location.name}", f"Defeat the {location.biome} threat"],
            QuestType.COLLECT: [f"Gather resources from {location.name}", f"Collect {location.biome} materials"],
            QuestType.EXPLORE: [f"Explore {location.name}", f"Discover the secrets of {location.name}"]
        }
        
        available_titles = titles.get(quest_type, ["Mysterious Quest"])
        return random.choice(available_titles)
    
    def _generate_quest_description(self, quest_type: QuestType, location: Location) -> str:
        """Generate quest description"""
        descriptions = {
            QuestType.KILL: f"Clear the dangerous creatures that have been terrorizing {location.name}.",
            QuestType.COLLECT: f"Gather valuable resources from the {location.biome} area of {location.name}.",
            QuestType.EXPLORE: f"Explore the mysterious {location.name} and discover its secrets."
        }
        
        return descriptions.get(quest_type, "A mysterious quest awaits.") 