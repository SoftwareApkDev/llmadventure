"""
Memory system for LLMAdventure
"""

import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

from ..utils.config import Config
from ..utils.logger import logger

class Memory:
    """Memory system for tracking game history and learning"""
    
    def __init__(self, config: Config):
        self.config = config
        self.memory_file = Path(config.get_data_dir()) / "memory.json"
        self.memories = []
        self.max_memories = 1000
        self.learning_rate = 0.1
        
    def add_memory(self, memory_type: str, data: Dict[str, Any], importance: float = 1.0):
        """Add a new memory"""
        memory = {
            "id": len(self.memories) + 1,
            "type": memory_type,
            "data": data,
            "importance": importance,
            "timestamp": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": None
        }
        
        self.memories.append(memory)
        
        # Keep memory size manageable
        if len(self.memories) > self.max_memories:
            self._prune_memories()
        
        logger.ai_event("Memory added", {"type": memory_type, "importance": importance})
    
    def get_relevant_memories(self, context: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Get memories relevant to current context"""
        relevant_memories = []
        
        for memory in self.memories:
            relevance_score = self._calculate_relevance(memory, context)
            if relevance_score > 0.3:  # Threshold for relevance
                memory_copy = memory.copy()
                memory_copy["relevance_score"] = relevance_score
                relevant_memories.append(memory_copy)
        
        # Sort by relevance and importance
        relevant_memories.sort(key=lambda x: x["relevance_score"] * x["importance"], reverse=True)
        
        # Update access statistics
        for memory in relevant_memories[:limit]:
            self._update_memory_access(memory["id"])
        
        return relevant_memories[:limit]
    
    def _calculate_relevance(self, memory: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate relevance score between memory and context"""
        score = 0.0
        
        # Check for matching keys
        for key in context:
            if key in memory["data"]:
                if isinstance(context[key], str) and isinstance(memory["data"][key], str):
                    # String similarity
                    if context[key].lower() in memory["data"][key].lower():
                        score += 0.3
                elif context[key] == memory["data"][key]:
                    # Exact match
                    score += 0.5
        
        # Check for similar memory types
        if "memory_type" in context and context["memory_type"] == memory["type"]:
            score += 0.2
        
        # Time decay factor
        time_diff = time.time() - datetime.fromisoformat(memory["timestamp"]).timestamp()
        time_decay = max(0.1, 1.0 - (time_diff / (24 * 3600)))  # Decay over days
        score *= time_decay
        
        return min(1.0, score)
    
    def _update_memory_access(self, memory_id: int):
        """Update memory access statistics"""
        for memory in self.memories:
            if memory["id"] == memory_id:
                memory["access_count"] += 1
                memory["last_accessed"] = datetime.now().isoformat()
                break
    
    def _prune_memories(self):
        """Remove least important memories"""
        # Sort by importance and access count
        self.memories.sort(key=lambda x: (x["importance"], x["access_count"]))
        
        # Remove bottom 20%
        remove_count = len(self.memories) // 5
        self.memories = self.memories[remove_count:]
        
        logger.ai_event("Memories pruned", {"removed_count": remove_count})
    
    def learn_from_experience(self, experience_type: str, outcome: str, 
                            context: Dict[str, Any], success: bool):
        """Learn from player experiences"""
        # Find similar past experiences
        similar_memories = self.get_relevant_memories(context, limit=3)
        
        # Update learning based on outcomes
        for memory in similar_memories:
            if memory["type"] == experience_type:
                # Adjust importance based on success/failure
                if success:
                    memory["importance"] += self.learning_rate
                else:
                    memory["importance"] -= self.learning_rate * 0.5
                
                memory["importance"] = max(0.1, min(2.0, memory["importance"]))
        
        # Add new experience memory
        experience_data = {
            "type": experience_type,
            "outcome": outcome,
            "success": success,
            "context": context
        }
        
        importance = 1.5 if not success else 1.0  # Remember failures more
        self.add_memory("experience", experience_data, importance)
    
    def get_player_patterns(self, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze player behavior patterns"""
        patterns = {
            "preferred_actions": {},
            "avoided_actions": {},
            "successful_strategies": {},
            "common_mistakes": {},
            "play_style": "balanced"
        }
        
        # Analyze memories for patterns
        for memory in self.memories:
            if memory["type"] == "player_action":
                action = memory["data"].get("action")
                success = memory["data"].get("success", True)
                
                if success:
                    patterns["preferred_actions"][action] = patterns["preferred_actions"].get(action, 0) + 1
                    patterns["successful_strategies"][action] = patterns["successful_strategies"].get(action, 0) + 1
                else:
                    patterns["avoided_actions"][action] = patterns["avoided_actions"].get(action, 0) + 1
                    patterns["common_mistakes"][action] = patterns["common_mistakes"].get(action, 0) + 1
        
        # Determine play style
        if patterns["preferred_actions"]:
            most_common = max(patterns["preferred_actions"].items(), key=lambda x: x[1])
            if "attack" in most_common[0].lower():
                patterns["play_style"] = "aggressive"
            elif "stealth" in most_common[0].lower():
                patterns["play_style"] = "stealthy"
            elif "magic" in most_common[0].lower():
                patterns["play_style"] = "magical"
        
        return patterns
    
    def save_memories(self):
        """Save memories to file"""
        try:
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.memory_file, 'w') as f:
                json.dump({
                    "memories": self.memories,
                    "max_memories": self.max_memories,
                    "learning_rate": self.learning_rate,
                    "last_saved": datetime.now().isoformat()
                }, f, indent=2)
            
            logger.ai_event("Memories saved", {"count": len(self.memories)})
            
        except Exception as e:
            logger.error(f"Error saving memories: {e}")
    
    def load_memories(self):
        """Load memories from file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                
                self.memories = data.get("memories", [])
                self.max_memories = data.get("max_memories", 1000)
                self.learning_rate = data.get("learning_rate", 0.1)
                
                logger.ai_event("Memories loaded", {"count": len(self.memories)})
            else:
                logger.info("No memory file found, starting fresh")
                
        except Exception as e:
            logger.error(f"Error loading memories: {e}")
            self.memories = []
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of memory system"""
        return {
            "total_memories": len(self.memories),
            "max_memories": self.max_memories,
            "learning_rate": self.learning_rate,
            "memory_types": self._count_memory_types(),
            "average_importance": sum(m["importance"] for m in self.memories) / max(1, len(self.memories)),
            "most_accessed": self._get_most_accessed_memories(5)
        }
    
    def _count_memory_types(self) -> Dict[str, int]:
        """Count memories by type"""
        counts = {}
        for memory in self.memories:
            memory_type = memory["type"]
            counts[memory_type] = counts.get(memory_type, 0) + 1
        return counts
    
    def _get_most_accessed_memories(self, limit: int) -> List[Dict[str, Any]]:
        """Get most frequently accessed memories"""
        sorted_memories = sorted(self.memories, key=lambda x: x["access_count"], reverse=True)
        return [
            {
                "id": m["id"],
                "type": m["type"],
                "access_count": m["access_count"],
                "importance": m["importance"]
            }
            for m in sorted_memories[:limit]
        ] 