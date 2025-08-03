"""
Inventory management for LLMAdventure
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class ItemType(Enum):
    """Types of items"""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    MATERIAL = "material"
    QUEST = "quest"


class ItemRarity(Enum):
    """Item rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Inventory:
    """Inventory management system"""

    def __init__(self):
        self.items = []
        self.max_items = 50
        self.gold = 0

    def add_item(self, item: Dict[str, Any]) -> bool:
        """Add item to inventory"""
        if len(self.items) >= self.max_items:
            return False

        self.items.append(item)
        return True

    def remove_item(self, item_name: str) -> Optional[Dict[str, Any]]:
        """Remove item from inventory by name"""
        for i, item in enumerate(self.items):
            if item["name"].lower() == item_name.lower():
                return self.items.pop(i)
        return None

    def get_item(self, item_name: str) -> Optional[Dict[str, Any]]:
        """Get item by name"""
        for item in self.items:
            if item["name"].lower() == item_name.lower():
                return item
        return None

    def has_item(self, item_name: str) -> bool:
        """Check if inventory has item"""
        return self.get_item(item_name) is not None

    def get_items_by_type(self, item_type: str) -> List[Dict[str, Any]]:
        """Get all items of a specific type"""
        return [item for item in self.items if item.get("type") == item_type]

    def get_equipped_items(self) -> Dict[str, Optional[Dict[str, Any]]]:
        """Get currently equipped items"""
        equipped = {}
        for item in self.items:
            if item.get("equipped", False):
                slot = item.get("slot", "unknown")
                equipped[slot] = item
        return equipped

    def equip_item(self, item_name: str) -> bool:
        """Equip an item"""
        item = self.get_item(item_name)
        if not item:
            return False

        slot = item.get("slot")
        if slot:
            for other_item in self.items:
                if (other_item.get("slot") == slot and
                        other_item.get("equipped", False)):
                    other_item["equipped"] = False

        item["equipped"] = True
        return True

    def unequip_item(self, item_name: str) -> bool:
        """Unequip an item"""
        item = self.get_item(item_name)
        if not item:
            return False

        item["equipped"] = False
        return True

    def get_inventory_summary(self) -> Dict[str, Any]:
        """Get inventory summary"""
        return {
            "total_items": len(self.items),
            "max_items": self.max_items,
            "gold": self.gold,
            "equipped_count": len([i for i in self.items if i.get("equipped", False)]),
            "item_types": self._count_item_types()
        }

    def _count_item_types(self) -> Dict[str, int]:
        """Count items by type"""
        counts = {}
        for item in self.items:
            item_type = item.get("type", "unknown")
            counts[item_type] = counts.get(item_type, 0) + 1
        return counts
