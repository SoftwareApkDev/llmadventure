#!/usr/bin/env python3
"""
Basic usage example for LLMAdventure

This example demonstrates how to use LLMAdventure programmatically
to create and play a text adventure game.
"""

import asyncio
from llmadventure.core.game import Game
from llmadventure.utils.config import Config
from llmadventure.utils.logger import logger


async def basic_game_example():
    """Demonstrate basic game functionality"""
    
    print("🎮 LLMAdventure Basic Example")
    print("=" * 40)

    config = Config()

    if not config.get_api_key():
        print("❌ No Google API key found!")
        print("Please set your GOOGLE_API_KEY environment variable")
        return

    game = Game(config)
    
    try:
        print("🚀 Starting new game...")
        await game.initialize_new_game("Hero", "warrior")
        
        print(f"✅ Game started! Welcome, {game.player.name}!")
        print(f"📍 Starting location: {game.player.location}")
        print(f"⚔️  Class: {game.player.player_class.value}")
        print(f"❤️  Health: {game.player.health}/{game.player.max_health}")

        print("\n👀 Looking around...")
        await game.look_around()

        print("\n🚶 Moving north...")
        await game.move_player("north")
        
        print("\n👀 Looking around again...")
        await game.look_around()

        print("\n📊 Player Status:")
        print(f"   Health: {game.player.health}/{game.player.max_health}")
        print(f"   Level: {game.player.level}")
        print(f"   Experience: {game.player.experience}")
        print(f"   Location: {game.player.location}")

        print("\n💾 Saving game...")
        await game.save_game("example_save")
        print("✅ Game saved!")

        state = game.get_game_state()
        print(f"\n📋 Game State Keys: {list(state.keys())}")
        
    except Exception as e:
        logger.error(f"Error in basic example: {e}")
        print(f"❌ Error: {e}")


async def combat_example():
    """Demonstrate combat functionality"""
    
    print("\n⚔️ Combat Example")
    print("=" * 40)
    
    config = Config()
    game = Game(config)
    
    try:
        await game.initialize_new_game("Fighter", "warrior")

        await game.look_around()

        if game.creatures_at_location:
            creature = game.creatures_at_location[0]
            print(f"\n⚔️ Attacking {creature.name}...")
            await game.attack_creature(creature.name)
        else:
            print("😴 No creatures to fight here...")
            
    except Exception as e:
        logger.error(f"Error in combat example: {e}")
        print(f"❌ Error: {e}")


async def inventory_example():
    """Demonstrate inventory management"""
    
    print("\n🎒 Inventory Example")
    print("=" * 40)
    
    config = Config()
    game = Game(config)
    
    try:
        await game.initialize_new_game("Collector", "rogue")

        await game.look_around()

        if game.items_at_location:
            item = game.items_at_location[0]
            print(f"\n🛍️ Taking {item.name}...")
            await game.take_item(item.name)

            print("\n🎒 Inventory:")
            for item in game.player.inventory.items:
                print(f"   - {item.name}: {item.description}")
        else:
            print("📦 No items to collect here...")
            
    except Exception as e:
        logger.error(f"Error in inventory example: {e}")
        print(f"❌ Error: {e}")


async def quest_example():
    """Demonstrate quest system"""
    
    print("\n📜 Quest Example")
    print("=" * 40)
    
    config = Config()
    game = Game(config)
    
    try:
        await game.initialize_new_game("Adventurer", "ranger")

        await game.look_around()

        if game.quests_available:
            print("\n📜 Available Quests:")
            for quest in game.quests_available:
                print(f"   - {quest.title}: {quest.description}")
        else:
            print("📋 No quests available here...")
            
    except Exception as e:
        logger.error(f"Error in quest example: {e}")
        print(f"❌ Error: {e}")


async def main():
    """Run all examples"""
    
    print("🎮 LLMAdventure Examples")
    print("=" * 50)

    await basic_game_example()

    await combat_example()

    await inventory_example()

    await quest_example()
    
    print("\n🎉 Examples completed!")
    print("For more examples, check out the documentation at:")
    print("https://docs.llmadventure.com/examples")


if __name__ == "__main__":
    asyncio.run(main())
