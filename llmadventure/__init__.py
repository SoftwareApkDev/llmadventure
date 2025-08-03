"""
LLMAdventure - A CLI-based text adventure game powered by Gemini 2.5 Flash
"""

__version__ = "0.1.0"
__author__ = "LLMAdventure Team"
__email__ = "dev@llmadventure.com"

from .core.game import Game
from .core.player import Player
from .core.creature import Creature
from .core.world import World
from .core.quest import Quest
from .core.inventory import Inventory

__all__ = [
    "Game",
    "Player", 
    "Creature",
    "World",
    "Quest",
    "Inventory",
] 