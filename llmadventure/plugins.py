"""
llmadventure.plugins

Defines the base Plugin class and plugin registration utilities.
"""
from typing import Type, Dict, Any, Callable

# Plugin registry
type_plugin_registry = Dict[str, Type['Plugin']]
plugin_registry: type_plugin_registry = {}

def register_plugin(cls: Type['Plugin']) -> Type['Plugin']:
    """Decorator to register a plugin class."""
    plugin_registry[cls.__name__] = cls
    return cls

class Plugin:
    """Base class for all plugins."""
    name: str = "Base Plugin"
    version: str = "0.0.1"
    description: str = "Base plugin class."

    def __init__(self):
        pass

    def activate(self, game: Any):
        """Activate the plugin with the game instance."""
        pass

    def deactivate(self, game: Any):
        """Deactivate the plugin from the game instance."""
        pass

