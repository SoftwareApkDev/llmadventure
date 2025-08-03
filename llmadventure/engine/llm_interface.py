"""
LLM Interface for Gemini 2.5 Flash integration
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Union
import google.generativeai as genai
from ..utils.logger import logger
from ..utils.config import Config

class LLMInterface:
    """Interface for Google Gemini 2.5 Flash model"""
    
    def __init__(self, config: Config):
        self.config = config
        self.model = None
        self.chat_history = []
        self.max_history = 50
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Gemini model"""
        try:
            api_key = self.config.get_api_key()
            if not api_key:
                logger.error("No Google API key found. Please set GOOGLE_API_KEY environment variable.")
                return
                
            genai.configure(api_key=api_key)
            
            model_config = self.config.get_model_config()
            self.model = genai.GenerativeModel(
                model_name=model_config["model"],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=model_config["max_tokens"],
                    temperature=model_config["temperature"],
                )
            )
            
            logger.info(f"LLM Interface initialized with model: {model_config['model']}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM model: {e}")
            self.model = None
    
    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.model is not None
    
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response from LLM"""
        if not self.is_available():
            return "LLM is not available. Please check your API key."
        
        try:
            # Build full prompt with context
            full_prompt = self._build_prompt(prompt, context)
            
            # Generate response
            response = await self._async_generate(full_prompt)
            
            # Add to chat history
            self._add_to_history(prompt, response)
            
            logger.ai_event("Generated response", {"prompt_length": len(prompt), "response_length": len(response)})
            return response
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return f"Error: {str(e)}"
    
    def _build_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build full prompt with context"""
        full_prompt = prompt
        
        if context:
            context_str = json.dumps(context, indent=2)
            full_prompt = f"Context:\n{context_str}\n\nPrompt:\n{prompt}"
        
        return full_prompt
    
    async def _async_generate(self, prompt: str) -> str:
        """Async wrapper for model generation"""
        loop = asyncio.get_event_loop()
        
        def generate():
            response = self.model.generate_content(prompt)
            return response.text
        
        return await loop.run_in_executor(None, generate)
    
    def _add_to_history(self, prompt: str, response: str):
        """Add interaction to chat history"""
        self.chat_history.append({
            "prompt": prompt,
            "response": response,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # Keep history within limit
        if len(self.chat_history) > self.max_history:
            self.chat_history.pop(0)
    
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """Get chat history"""
        return self.chat_history.copy()
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history.clear()
    
    async def generate_story_segment(self, 
                                   location: str, 
                                   player_state: Dict[str, Any],
                                   world_context: Dict[str, Any]) -> str:
        """Generate story segment for current location"""
        prompt = f"""
        You are a master storyteller creating an immersive text adventure game.
        
        Current Location: {location}
        Player State: {json.dumps(player_state, indent=2)}
        World Context: {json.dumps(world_context, indent=2)}
        
        Create a vivid, atmospheric description of this location that draws the player in.
        Include:
        - Sensory details (sights, sounds, smells)
        - Environmental atmosphere
        - Potential dangers or opportunities
        - Hints about what might be nearby
        
        Keep it concise but evocative (2-3 paragraphs max).
        """
        
        return await self.generate_response(prompt)
    
    async def generate_creature_description(self, 
                                          creature: Dict[str, Any],
                                          encounter_context: Dict[str, Any]) -> str:
        """Generate creature encounter description"""
        prompt = f"""
        You are describing a creature encounter in a text adventure game.
        
        Creature: {json.dumps(creature, indent=2)}
        Encounter Context: {json.dumps(encounter_context, indent=2)}
        
        Create a vivid description of this creature as the player encounters it.
        Include:
        - Physical appearance and demeanor
        - Behavioral cues (hostile, curious, fearful, etc.)
        - Environmental context
        - Any special abilities or characteristics
        
        Make it engaging and atmospheric (1-2 paragraphs).
        """
        
        return await self.generate_response(prompt)
    
    async def generate_combat_narrative(self,
                                      player_action: str,
                                      creature_action: str,
                                      combat_state: Dict[str, Any]) -> str:
        """Generate combat narrative"""
        prompt = f"""
        You are narrating a combat scene in a text adventure game.
        
        Player Action: {player_action}
        Creature Action: {creature_action}
        Combat State: {json.dumps(combat_state, indent=2)}
        
        Create an exciting, dynamic description of this combat round.
        Include:
        - Vivid action descriptions
        - Environmental details
        - Tension and drama
        - Clear outcome of the actions
        
        Make it cinematic and engaging (1 paragraph).
        """
        
        return await self.generate_response(prompt)
    
    async def generate_dialogue_response(self,
                                       npc_data: Dict[str, Any],
                                       player_input: str,
                                       conversation_context: Dict[str, Any]) -> str:
        """Generate NPC dialogue response"""
        prompt = f"""
        You are roleplaying an NPC in a text adventure game.
        
        NPC: {json.dumps(npc_data, indent=2)}
        Player Input: "{player_input}"
        Conversation Context: {json.dumps(conversation_context, indent=2)}
        
        Respond as this NPC would naturally speak.
        Consider:
        - NPC's personality and background
        - Current situation and context
        - Player's reputation and actions
        - NPC's goals and motivations
        
        Keep the response natural and in-character (1-2 sentences).
        """
        
        return await self.generate_response(prompt)
    
    async def generate_quest_description(self,
                                       quest_data: Dict[str, Any],
                                       world_context: Dict[str, Any]) -> str:
        """Generate quest description"""
        prompt = f"""
        You are describing a quest in a text adventure game.
        
        Quest: {json.dumps(quest_data, indent=2)}
        World Context: {json.dumps(world_context, indent=2)}
        
        Create an engaging quest description that motivates the player.
        Include:
        - Clear objectives
        - Potential rewards
        - Story context and background
        - Hints about difficulty or requirements
        
        Make it compelling and clear (2-3 paragraphs).
        """
        
        return await self.generate_response(prompt)
    
    async def generate_world_location(self,
                                    biome: str,
                                    difficulty: int,
                                    world_seed: int) -> Dict[str, Any]:
        """Generate procedural world location"""
        prompt = f"""
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
        
        response = await self.generate_response(prompt)
        
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                logger.warning("Could not extract JSON from LLM response")
                return self._get_fallback_location(biome, difficulty)
                
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in LLM response: {e}")
            return self._get_fallback_location(biome, difficulty)
    
    def _get_fallback_location(self, biome: str, difficulty: int) -> Dict[str, Any]:
        """Fallback location generation when LLM fails"""
        return {
            "name": f"{biome.title()} Area",
            "description": f"A mysterious {biome} area.",
            "features": ["Unknown terrain"],
            "creatures": [],
            "items": [],
            "hazards": [],
            "connections": ["north", "south", "east", "west"]
        }
    
    def update_config(self, new_config: Dict[str, Any]):
        """Update LLM configuration"""
        for key, value in new_config.items():
            self.config.set(key, value)
        
        # Reinitialize model with new config
        self._initialize_model() 