"""
Prompt templates for LLM interactions in LLMAdventure
"""

from typing import Dict, Any, List

class PromptTemplates:
    """Collection of prompt templates for different game scenarios"""
    
    @staticmethod
    def location_description(location_name: str, biome: str, features: List[str], 
                           player_context: Dict[str, Any]) -> str:
        """Template for location description generation"""
        return f"""
        You are a master storyteller creating an immersive text adventure game.
        
        Location: {location_name}
        Biome: {biome}
        Features: {', '.join(features)}
        Player Context: {player_context}
        
        Create a vivid, atmospheric description of this location that draws the player in.
        Include:
        - Sensory details (sights, sounds, smells)
        - Environmental atmosphere
        - Potential dangers or opportunities
        - Hints about what might be nearby
        
        Keep it concise but evocative (2-3 paragraphs max).
        """
    
    @staticmethod
    def creature_encounter(creature_name: str, creature_type: str, 
                         creature_stats: Dict[str, Any], location: str) -> str:
        """Template for creature encounter description"""
        return f"""
        You are describing a creature encounter in a text adventure game.
        
        Creature: {creature_name}
        Type: {creature_type}
        Stats: {creature_stats}
        Location: {location}
        
        Create a vivid description of this creature as the player encounters it.
        Include:
        - Physical appearance and demeanor
        - Behavioral cues (hostile, curious, fearful, etc.)
        - Environmental context
        - Any special abilities or characteristics
        
        Make it engaging and atmospheric (1-2 paragraphs).
        """
    
    @staticmethod
    def combat_narrative(player_action: str, creature_action: str, 
                        combat_state: Dict[str, Any]) -> str:
        """Template for combat narrative generation"""
        return f"""
        You are narrating a combat scene in a text adventure game.
        
        Player Action: {player_action}
        Creature Action: {creature_action}
        Combat State: {combat_state}
        
        Create an exciting, dynamic description of this combat round.
        Include:
        - Vivid action descriptions
        - Environmental details
        - Tension and drama
        - Clear outcome of the actions
        
        Make it cinematic and engaging (1 paragraph).
        """
    
    @staticmethod
    def npc_dialogue(npc_name: str, npc_data: Dict[str, Any], 
                    player_input: str, context: Dict[str, Any]) -> str:
        """Template for NPC dialogue generation"""
        return f"""
        You are roleplaying an NPC in a text adventure game.
        
        NPC: {npc_name}
        NPC Data: {npc_data}
        Player Input: "{player_input}"
        Context: {context}
        
        Respond as this NPC would naturally speak.
        Consider:
        - NPC's personality and background
        - Current situation and context
        - Player's reputation and actions
        - NPC's goals and motivations
        
        Keep the response natural and in-character (1-2 sentences).
        """
    
    @staticmethod
    def quest_description(quest_title: str, quest_type: str, 
                         objectives: List[str], rewards: Dict[str, Any]) -> str:
        """Template for quest description generation"""
        return f"""
        You are describing a quest in a text adventure game.
        
        Quest: {quest_title}
        Type: {quest_type}
        Objectives: {objectives}
        Rewards: {rewards}
        
        Create an engaging quest description that motivates the player.
        Include:
        - Clear objectives
        - Potential rewards
        - Story context and background
        - Hints about difficulty or requirements
        
        Make it compelling and clear (2-3 paragraphs).
        """
    
    @staticmethod
    def world_generation(biome: str, difficulty: int, world_seed: int) -> str:
        """Template for procedural world generation"""
        return f"""
        You are generating a procedural location for a text adventure game.
        
        Biome: {biome}
        Difficulty Level: {difficulty}
        World Seed: {world_seed}
        
        Generate a JSON object describing this location with:
        - name: Location name
        - description: Brief description
        - features: List of notable features
        - creatures: List of possible creatures (with types and levels)
        - items: List of possible items
        - hazards: List of environmental hazards
        - connections: List of connected locations (north, south, east, west)
        
        Return only valid JSON, no additional text.
        """
    
    @staticmethod
    def story_segment(location: str, player_state: Dict[str, Any], 
                     world_context: Dict[str, Any]) -> str:
        """Template for story segment generation"""
        return f"""
        You are a master storyteller creating an immersive text adventure game.
        
        Current Location: {location}
        Player State: {player_state}
        World Context: {world_context}
        
        Create a vivid, atmospheric description of this location that draws the player in.
        Include:
        - Sensory details (sights, sounds, smells)
        - Environmental atmosphere
        - Potential dangers or opportunities
        - Hints about what might be nearby
        
        Keep it concise but evocative (2-3 paragraphs max).
        """
    
    @staticmethod
    def item_description(item_name: str, item_type: str, 
                        item_properties: Dict[str, Any]) -> str:
        """Template for item description generation"""
        return f"""
        You are describing an item in a text adventure game.
        
        Item: {item_name}
        Type: {item_type}
        Properties: {item_properties}
        
        Create a vivid description of this item.
        Include:
        - Physical appearance
        - Magical properties (if any)
        - Historical significance
        - Practical uses
        
        Make it engaging and informative (1 paragraph).
        """
    
    @staticmethod
    def puzzle_hint(puzzle_type: str, difficulty: int, 
                   player_progress: Dict[str, Any]) -> str:
        """Template for puzzle hint generation"""
        return f"""
        You are providing a hint for a puzzle in a text adventure game.
        
        Puzzle Type: {puzzle_type}
        Difficulty: {difficulty}
        Player Progress: {player_progress}
        
        Provide a helpful but not too obvious hint.
        Consider:
        - Player's current progress
        - Puzzle difficulty
        - Available clues
        - Logical next steps
        
        Keep it concise and helpful (1-2 sentences).
        """
    
    @staticmethod
    def weather_description(location: str, season: str, 
                          weather_conditions: Dict[str, Any]) -> str:
        """Template for weather description generation"""
        return f"""
        You are describing the weather and atmosphere in a text adventure game.
        
        Location: {location}
        Season: {season}
        Weather Conditions: {weather_conditions}
        
        Create an atmospheric weather description.
        Include:
        - Current weather conditions
        - Environmental effects
        - Impact on visibility and movement
        - Atmospheric mood
        
        Make it immersive and atmospheric (1 paragraph).
        """
    
    @staticmethod
    def character_development(player_name: str, player_class: str, 
                            player_stats: Dict[str, Any], 
                            recent_events: List[str]) -> str:
        """Template for character development narrative"""
        return f"""
        You are narrating character development in a text adventure game.
        
        Player: {player_name}
        Class: {player_class}
        Stats: {player_stats}
        Recent Events: {recent_events}
        
        Create a narrative about the player's growth and development.
        Include:
        - Reflection on recent experiences
        - Growth in abilities and skills
        - Character development moments
        - Future potential
        
        Make it personal and engaging (1-2 paragraphs).
        """ 