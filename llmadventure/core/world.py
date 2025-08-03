"""
World management for LLMAdventure
"""

import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from ..utils.config import Config
from ..utils.logger import logger

@dataclass
class Location:
    """Represents a location in the world"""
    name: str
    description: str
    biome: str
    difficulty: int
    coordinates: Tuple[int, int]
    features: List[str]
    connections: Dict[str, Optional[Tuple[int, int]]]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "biome": self.biome,
            "difficulty": self.difficulty,
            "coordinates": self.coordinates,
            "features": self.features,
            "connections": self.connections
        }


class World:
    """Manages the game world and locations"""

    def __init__(self, config: Config):
        self.config = config
        self.seed = random.randint(1, 1000000)
        self.locations = {}
        self.biomes = ["forest", "mountain", "desert", "swamp", "plains", "cave", "ruins"]

    async def initialize_world(self):
        """Initialize the world with starting location"""
        starting_location = Location(
            name="Village Square",
            description="A peaceful village square with a central fountain.",
            biome="plains",
            difficulty=1,
            coordinates=(0, 0),
            features=["fountain", "market", "inn"],
            connections={"north": None, "south": None, "east": None, "west": None}
        )

        self.locations[(0, 0)] = starting_location
        logger.game_event("World initialized", {"seed": self.seed})

    async def generate_location(self, coordinates: Tuple[int, int]):
        """Generate a new location at given coordinates"""
        if coordinates in self.locations:
            return self.locations[coordinates]

        random.seed(self.seed + coordinates[0] * 1000 + coordinates[1])

        biome = self._get_biome_for_coordinates(coordinates)
        difficulty = self._calculate_difficulty(coordinates)
        
        location = Location(
            name=self._generate_location_name(biome, coordinates),
            description=f"A {biome} area.",
            biome=biome,
            difficulty=difficulty,
            coordinates=coordinates,
            features=self._generate_features(biome),
            connections=self._generate_connections(coordinates)
        )
        
        self.locations[coordinates] = location
        logger.game_event("Location generated", {
            "coordinates": coordinates,
            "name": location.name,
            "biome": biome
        })
        
        return location
    
    def get_location(self, coordinates: Tuple[int, int]) -> Optional[Location]:
        """Get location at coordinates"""
        return self.locations.get(coordinates)
    
    def has_location(self, coordinates: Tuple[int, int]) -> bool:
        """Check if location exists at coordinates"""
        return coordinates in self.locations
    
    def _get_biome_for_coordinates(self, coordinates: Tuple[int, int]) -> str:
        """Determine biome based on coordinates"""
        x, y = coordinates
        distance = abs(x) + abs(y)
        
        if distance == 0:
            return "plains"
        elif distance <= 2:
            return random.choice(["forest", "plains"])
        elif distance <= 5:
            return random.choice(["forest", "mountain", "swamp"])
        else:
            return random.choice(["mountain", "desert", "cave", "ruins"])
    
    def _calculate_difficulty(self, coordinates: Tuple[int, int]) -> int:
        """Calculate difficulty based on distance from center"""
        x, y = coordinates
        distance = abs(x) + abs(y)
        return min(10, max(1, distance // 2 + 1))
    
    def _generate_location_name(self, biome: str, coordinates: Tuple[int, int]) -> str:
        """Generate a name for the location"""
        x, y = coordinates
        
        if coordinates == (0, 0):
            return "Village Square"
        
        biome_names = {
            "forest": ["Dark Woods", "Mystic Grove", "Ancient Forest", "Whispering Woods"],
            "mountain": ["Rocky Peak", "Misty Summit", "Stone Ridge", "Echo Mountain"],
            "desert": ["Sandy Dunes", "Burning Sands", "Desert Wastes", "Sun-scorched Plains"],
            "swamp": ["Misty Bog", "Dark Marsh", "Fetid Swamp", "Shadowy Wetlands"],
            "plains": ["Rolling Hills", "Golden Fields", "Open Prairie", "Grassy Plains"],
            "cave": ["Dark Cavern", "Crystal Cave", "Ancient Tunnels", "Shadowy Depths"],
            "ruins": ["Ancient Ruins", "Forgotten Temple", "Crumbling Tower", "Lost City"]
        }
        
        names = biome_names.get(biome, ["Unknown Area"])
        return random.choice(names)
    
    def _generate_features(self, biome: str) -> List[str]:
        """Generate features for the location"""
        biome_features = {
            "forest": ["trees", "stream", "clearing", "fallen logs"],
            "mountain": ["rocks", "cliff", "cave entrance", "mountain path"],
            "desert": ["sand dunes", "rock formations", "oasis", "ancient bones"],
            "swamp": ["mud", "water", "reeds", "fallen trees"],
            "plains": ["grass", "flowers", "small hill", "ancient road"],
            "cave": ["stalactites", "crystal formations", "underground stream", "ancient markings"],
            "ruins": ["broken walls", "carved stones", "ancient artifacts", "mysterious symbols"]
        }
        
        features = biome_features.get(biome, [])
        return random.sample(features, min(2, len(features)))
    
    def _generate_connections(self, coordinates: Tuple[int, int]) -> Dict[str, Optional[Tuple[int, int]]]:
        """Generate connections to other locations"""
        x, y = coordinates
        
        connections = {
            "north": (x, y - 1),
            "south": (x, y + 1),
            "east": (x + 1, y),
            "west": (x - 1, y)
        }
        
        return connections
    
    def get_context_for_location(self, coordinates: Tuple[int, int]) -> Dict[str, Any]:
        """Get world context for a location"""
        location = self.get_location(coordinates)
        if not location:
            return {}

        nearby = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nearby_coords = (coordinates[0] + dx, coordinates[1] + dy)
                nearby_loc = self.get_location(nearby_coords)
                if nearby_loc:
                    nearby.append({
                        "name": nearby_loc.name,
                        "biome": nearby_loc.biome,
                        "direction": self._get_direction(coordinates, nearby_coords)
                    })
        
        return {
            "location": {
                "name": location.name,
                "biome": location.biome,
                "difficulty": location.difficulty,
                "features": location.features
            },
            "nearby": nearby,
            "world_seed": self.seed
        }
    
    def _get_direction(self, from_coords: Tuple[int, int], to_coords: Tuple[int, int]) -> str:
        """Get direction from one coordinate to another"""
        dx = to_coords[0] - from_coords[0]
        dy = to_coords[1] - from_coords[1]
        
        if dx == 1:
            return "east"
        elif dx == -1:
            return "west"
        elif dy == 1:
            return "south"
        elif dy == -1:
            return "north"
        else:
            return "unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert world to dictionary"""
        return {
            "seed": self.seed,
            "locations": {
                str(coords): {
                    "name": loc.name,
                    "description": loc.description,
                    "biome": loc.biome,
                    "difficulty": loc.difficulty,
                    "coordinates": loc.coordinates,
                    "features": loc.features,
                    "connections": {k: str(v) if v else None for k, v in loc.connections.items()}
                }
                for coords, loc in self.locations.items()
            }
        }
    
    async def load_from_dict(self, data: Dict[str, Any]):
        """Load world from dictionary"""
        self.seed = data["seed"]
        self.locations = {}
        
        for coords_str, loc_data in data["locations"].items():
            coords = tuple(map(int, coords_str.strip("()").split(", ")))
            
            connections = {}
            for direction, conn_str in loc_data["connections"].items():
                if conn_str:
                    connections[direction] = tuple(map(int, conn_str.strip("()").split(", ")))
                else:
                    connections[direction] = None
            
            location = Location(
                name=loc_data["name"],
                description=loc_data["description"],
                biome=loc_data["biome"],
                difficulty=loc_data["difficulty"],
                coordinates=coords,
                features=loc_data["features"],
                connections=connections
            )
            
            self.locations[coords] = location
