"""
Tests for the main Game class
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import tempfile

from llmadventure.core.game import Game
from llmadventure.core.player import Player, PlayerClass
from llmadventure.core.creature import Creature
from llmadventure.core.quest import Quest
from llmadventure.utils.config import Config


class TestGame:
    """Test cases for the Game class"""
    
    @pytest.fixture
    def config(self):
        """Create a test configuration"""
        config = Config()
        config.api_key = "test_api_key"
        return config
    
    @pytest.fixture
    def game(self, config):
        """Create a test game instance"""
        return Game(config)
    
    @pytest.fixture
    def mock_llm(self):
        """Create a mock LLM interface"""
        mock = AsyncMock()
        mock.generate_response.return_value = "Test response"
        mock.generate_location.return_value = {
            "name": "Test Location",
            "description": "A test location",
            "creatures": [],
            "items": [],
            "exits": ["north", "south"]
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_game_initialization(self, game, config):
        """Test that a new game initializes correctly"""
        player_name = "TestPlayer"
        player_class = "warrior"

        await game.initialize_new_game(player_name, player_class)

        assert game.player is not None
        assert game.player.name == player_name
        assert game.player.player_class == PlayerClass.WARRIOR
        assert game.world is not None
        assert game.combat is not None
        assert game.game_running is True
        assert game.player.location == (0, 0)
    
    @pytest.mark.asyncio
    async def test_game_initialization_invalid_class(self, game):
        """Test that invalid player class raises an error"""
        player_name = "TestPlayer"
        invalid_class = "invalid_class"

        with pytest.raises(ValueError):
            await game.initialize_new_game(player_name, invalid_class)
    
    @pytest.mark.asyncio
    async def test_save_and_load_game(self, game, config):
        """Test saving and loading a game"""
        await game.initialize_new_game("TestPlayer", "warrior")
        game.player.health = 50
        game.player.experience = 100
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            save_file = f.name
        
        try:
            await game.save_game(save_file)

            new_game = Game(config)

            await new_game.load_game(save_file)

            assert new_game.player.name == "TestPlayer"
            assert new_game.player.health == 50
            assert new_game.player.experience == 100
            assert new_game.player.player_class == PlayerClass.WARRIOR
            
        finally:
            Path(save_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_move_player(self, game, mock_llm):
        """Test player movement"""
        with patch.object(game, 'llm', mock_llm):
            await game.initialize_new_game("TestPlayer", "warrior")
            initial_location = game.player.location

            await game.move_player("north")

            assert game.player.location != initial_location
            assert game.player.location == (0, 1)
    
    @pytest.mark.asyncio
    async def test_move_player_invalid_direction(self, game):
        """Test that invalid movement direction is handled"""
        await game.initialize_new_game("TestPlayer", "warrior")

        with pytest.raises(ValueError):
            await game.move_player("invalid")
    
    @pytest.mark.asyncio
    async def test_look_around(self, game, mock_llm):
        """Test looking around functionality"""
        with patch.object(game, 'llm', mock_llm):
            await game.initialize_new_game("TestPlayer", "warrior")

            await game.look_around()

            mock_llm.generate_location.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_attack_creature(self, game):
        """Test attacking a creature"""
        await game.initialize_new_game("TestPlayer", "warrior")
        creature = Creature("Test Creature", 50, 10, 5)
        game.creatures_at_location = [creature]

        initial_health = creature.health
        await game.attack_creature("Test Creature")

        assert creature.health < initial_health

    @pytest.mark.asyncio
    async def test_attack_nonexistent_creature(self, game):
        """Test attacking a creature that doesn't exist"""
        await game.initialize_new_game("TestPlayer", "warrior")
        game.creatures_at_location = []

        with pytest.raises(ValueError):
            await game.attack_creature("Nonexistent Creature")
    
    @pytest.mark.asyncio
    async def test_take_item(self, game):
        """Test taking an item"""
        await game.initialize_new_game("TestPlayer", "warrior")
        item = {"name": "Test Item", "description": "A test item", "type": "weapon"}
        game.items_at_location = [item]

        await game.take_item("Test Item")

        assert len(game.items_at_location) == 0
        assert any(item["name"] == "Test Item" for item in game.player.inventory.items)
    
    @pytest.mark.asyncio
    async def test_take_nonexistent_item(self, game):
        """Test taking an item that doesn't exist"""
        await game.initialize_new_game("TestPlayer", "warrior")
        game.items_at_location = []

        with pytest.raises(ValueError):
            await game.take_item("Nonexistent Item")
    
    @pytest.mark.asyncio
    async def test_use_item(self, game):
        """Test using an item"""
        await game.initialize_new_game("TestPlayer", "warrior")
        item = {"name": "Health Potion", "description": "Restores health", "type": "consumable"}
        game.player.inventory.add_item(item)

        await game.use_item("Health Potion")

        assert not any(item["name"] == "Health Potion" for item in game.player.inventory.items)
    
    @pytest.mark.asyncio
    async def test_use_nonexistent_item(self, game):
        """Test using an item that doesn't exist"""
        await game.initialize_new_game("TestPlayer", "warrior")

        with pytest.raises(ValueError):
            await game.use_item("Nonexistent Item")
    
    @pytest.mark.asyncio
    async def test_process_command(self, game):
        """Test processing custom commands"""
        await game.initialize_new_game("TestPlayer", "warrior")

        result = await game.process_command("custom_command")

        assert result is not None
    
    @pytest.mark.asyncio
    async def test_auto_save(self, game):
        """Test auto-save functionality"""
        await game.initialize_new_game("TestPlayer", "warrior")
        game.auto_save_enabled = True

        await game.move_player("north")

        await asyncio.sleep(0.1)

        assert game.save_file is not None
    
    @pytest.mark.asyncio
    async def test_player_death(self, game):
        """Test player death handling"""
        await game.initialize_new_game("TestPlayer", "warrior")
        game.player.health = 1

        await game._handle_player_death()

        assert game.game_running is False
    
    @pytest.mark.asyncio
    async def test_creature_death(self, game):
        """Test creature death handling"""
        await game.initialize_new_game("TestPlayer", "warrior")
        creature = Creature("Test Creature", 1, 10, 5)
        game.creatures_at_location = [creature]

        await game._handle_creature_death(creature)

        assert creature not in game.creatures_at_location
        assert game.player.experience > 0
    
    def test_get_player_state(self, game):
        """Test getting player state"""
        game.player = Player("TestPlayer", PlayerClass.WARRIOR)
        game.player.health = 75
        game.player.experience = 150

        state = game._get_player_state()

        assert state["name"] == "TestPlayer"
        assert state["health"] == 75
        assert state["experience"] == 150
        assert state["player_class"] == "warrior"
    
    def test_get_game_state(self, game):
        """Test getting complete game state"""
        game.player = Player("TestPlayer", PlayerClass.WARRIOR)
        game.game_running = True
        game.current_location = {"name": "Test Location"}

        state = game.get_game_state()

        assert "player" in state
        assert "game_running" in state
        assert "current_location" in state
        assert state["game_running"] is True
    
    @pytest.mark.asyncio
    async def test_generate_location_content(self, game, mock_llm):
        """Test location content generation"""
        with patch.object(game, 'llm', mock_llm):
            await game.initialize_new_game("TestPlayer", "warrior")

            await game._generate_location_content()

            mock_llm.generate_location.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_game_with_plugins(self, game):
        """Test game with plugin system"""
        await game.initialize_new_game("TestPlayer", "warrior")

        mock_plugin = Mock()
        game.plugins = [mock_plugin]

        await game.move_player("north")

        mock_plugin.on_player_move.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_error_handling(self, game):
        """Test error handling in game operations"""
        await game.initialize_new_game("TestPlayer", "warrior")

        with patch.object(game.llm, 'generate_response', side_effect=Exception("API Error")):
            with pytest.raises(Exception):
                await game.look_around()
    
    @pytest.mark.asyncio
    async def test_performance_optimization(self, game):
        """Test that game operations are performant"""
        await game.initialize_new_game("TestPlayer", "warrior")

        import time
        start_time = time.time()
        
        for _ in range(10):
            await game.move_player("north")
            await game.move_player("south")
        
        end_time = time.time()

        assert end_time - start_time < 1.0
    
    @pytest.mark.asyncio
    async def test_memory_efficiency(self, game):
        """Test that game doesn't leak memory"""
        import gc

        initial_objects = len(gc.get_objects())
        
        for _ in range(5):
            await game.initialize_new_game("TestPlayer", "warrior")
            await game.move_player("north")
            await game.look_around()

            gc.collect()
        
        final_objects = len(gc.get_objects())

        assert final_objects - initial_objects < 1000


class TestGameIntegration:
    """Integration tests for the Game class"""
    
    @pytest.mark.asyncio
    async def test_full_game_session(self, config):
        """Test a complete game session"""
        game = Game(config)

        await game.initialize_new_game("IntegrationTest", "mage")

        await game.move_player("north")
        await game.move_player("east")
        await game.move_player("south")
        await game.move_player("west")

        await game.look_around()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            save_file = f.name
        
        try:
            await game.save_game(save_file)

            new_game = Game(config)
            await new_game.load_game(save_file)

            assert new_game.player.name == "IntegrationTest"
            assert new_game.player.player_class == PlayerClass.MAGE
            assert new_game.game_running is True
            
        finally:
            Path(save_file).unlink(missing_ok=True)
    
    @pytest.mark.asyncio
    async def test_combat_integration(self, config):
        """Test combat system integration"""
        game = Game(config)
        await game.initialize_new_game("CombatTest", "warrior")

        creature = Creature("Test Dragon", 100, 15, 10)
        game.creatures_at_location = [creature]

        initial_health = creature.health
        await game.attack_creature("Test Dragon")

        assert creature.health < initial_health
        assert game.player.experience > 0
    
    @pytest.mark.asyncio
    async def test_quest_integration(self, config):
        """Test quest system integration"""
        game = Game(config)
        await game.initialize_new_game("QuestTest", "ranger")

        quest = Quest(
            title="Test Quest",
            description="A test quest",
            quest_type="combat",
            target_count=1,
            reward_exp=50
        )
        game.quests_available = [quest]

        quest.progress = 1
        await game._handle_quest_completion(quest)

        assert game.player.experience >= 50
