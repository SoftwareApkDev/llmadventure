"""
Main CLI entry point for LLMAdventure
"""

import sys
import asyncio
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from llmadventure.core.game import Game
from llmadventure.utils.config import Config
from llmadventure.utils.logger import logger
from llmadventure.cli.menus import MenuSystem
from llmadventure.cli.display import DisplayManager

app = typer.Typer()
console = Console()


def main():
    """Main entry point for LLMAdventure"""
    try:
        config = Config()
        if not config.get_api_key():
            console.print(Panel(
                "[red]No Google API key found![/red]\n\n"
                "Please set your Google API key:\n"
                "1. Get a key from https://makersuite.google.com/app/apikey\n"
                "2. Set environment variable: export GOOGLE_API_KEY=your_key\n"
                "3. Or create a .env file with: GOOGLE_API_KEY=your_key",
                title="[bold red]API Key Required[/bold red]",
                border_style="red"
            ))
            sys.exit(1)

        show_welcome_screen()
        display = DisplayManager()
        menu_system = MenuSystem(display)
        asyncio.run(run_game(config, display, menu_system))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Game interrupted. Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)


def show_welcome_screen():
    """Display the welcome screen"""
    welcome_text = Text()
    welcome_text.append("LLM", style="bold blue")
    welcome_text.append("Adventure", style="bold green")
    welcome_text.append("\n\n", style="default")
    welcome_text.append("A CLI-based text adventure game powered by Gemini 2.5 Flash\n", style="italic")
    welcome_text.append("Embark on procedurally generated quests and explore dynamic worlds!\n\n", style="default")
    welcome_text.append("Press Enter to begin your adventure...", style="yellow")
    
    console.print(Panel(
        welcome_text,
        title="[bold]Welcome to[/bold]",
        border_style="blue",
        padding=(1, 2)
    ))
    
    input()


async def run_game(config: Config, display: DisplayManager, menu_system: MenuSystem):
    """Main game loop"""
    game = None
    
    while True:
        try:
            choice = await menu_system.show_main_menu()
            
            if choice == "new_game":
                game = await start_new_game(config)
                if game:
                    await play_game(game, display)
                    
            elif choice == "load_game":
                game = await load_game(config)
                if game:
                    await play_game(game, display)
                    
            elif choice == "settings":
                await menu_system.show_settings_menu(config)
                
            elif choice == "help":
                await menu_system.show_help()
                
            elif choice == "quit":
                console.print("[yellow]Thanks for playing LLMAdventure![/yellow]")
                break
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Returning to main menu...[/yellow]")
            continue
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            console.print(f"[red]Error: {e}[/red]")
            continue


async def start_new_game(config: Config) -> Optional[Game]:
    """Start a new game"""
    try:
        console.print("\n[bold blue]Character Creation[/bold blue]")
        
        name = console.input("[cyan]Enter your character's name: [/cyan]").strip()
        if not name:
            name = "Adventurer"

        classes = ["Warrior", "Mage", "Rogue", "Ranger"]
        console.print("\n[bold]Choose your class:[/bold]")
        for i, class_name in enumerate(classes, 1):
            console.print(f"{i}. {class_name}")
        
        while True:
            try:
                choice = int(console.input("\n[cyan]Enter your choice (1-4): [/cyan]"))
                if 1 <= choice <= 4:
                    player_class = classes[choice - 1].lower()
                    break
                else:
                    console.print("[red]Please enter a number between 1 and 4.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")

        game = Game(config)
        await game.initialize_new_game(name, player_class)
        
        console.print(f"\n[green]Welcome, {name} the {player_class.title()}![/green]")
        console.print("[yellow]Your adventure begins...[/yellow]\n")
        
        return game
        
    except Exception as e:
        logger.error(f"Error starting new game: {e}")
        console.print(f"[red]Error starting new game: {e}[/red]")
        return None


async def load_game(config: Config) -> Optional[Game]:
    """Load an existing game"""
    try:
        save_dir = Path(config.get_data_dir()) / "saves"
        save_dir.mkdir(exist_ok=True)
        
        save_files = list(save_dir.glob("*.json"))
        
        if not save_files:
            console.print("[yellow]No save files found.[/yellow]")
            return None

        console.print("\n[bold blue]Load Game[/bold blue]")
        console.print("[bold]Available saves:[/bold]")
        
        for i, save_file in enumerate(save_files, 1):
            console.print(f"{i}. {save_file.stem}")

        while True:
            try:
                choice = int(console.input(f"\n[cyan]Enter your choice (1-{len(save_files)}): [/cyan]"))
                if 1 <= choice <= len(save_files):
                    selected_file = save_files[choice - 1]
                    break
                else:
                    console.print(f"[red]Please enter a number between 1 and {len(save_files)}.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")

        game = Game(config)
        await game.load_game(str(selected_file))
        console.print(f"\n[green]Game loaded: {selected_file.stem}[/green]")
        return game
        
    except Exception as e:
        logger.error(f"Error loading game: {e}")
        console.print(f"[red]Error loading game: {e}[/red]")
        return None


async def play_game(game: Game, display: DisplayManager):
    """Main game play loop"""
    try:
        while True:
            await display.show_game_state(game)

            command = console.input("\n[cyan]What would you like to do? [/cyan]").strip().lower()
            
            if command in ["quit", "exit", "q"]:
                await game.save_game()
                console.print("[yellow]Game saved. Returning to main menu...[/yellow]")
                break
                
            elif command in ["save", "s"]:
                await game.save_game()
                console.print("[green]Game saved![/green]")
                
            elif command in ["help", "h", "?"]:
                await display.show_help()
                
            elif command in ["inventory", "i", "inv"]:
                await display.show_inventory(game.player)
                
            elif command in ["status", "stats", "st"]:
                await display.show_player_status(game.player)
                
            elif command in ["look", "l"]:
                await game.look_around()
                
            elif command in ["north", "n"]:
                await game.move_player("north")
            elif command in ["south", "s"]:
                await game.move_player("south")
            elif command in ["east", "e"]:
                await game.move_player("east")
            elif command in ["west", "w"]:
                await game.move_player("west")
                
            elif command.startswith("attack "):
                target = command[7:].strip()
                await game.attack_creature(target)
                
            elif command.startswith("talk "):
                npc = command[5:].strip()
                await game.talk_to_npc(npc)
                
            elif command.startswith("use "):
                item = command[4:].strip()
                await game.use_item(item)
                
            elif command.startswith("take "):
                item = command[5:].strip()
                await game.take_item(item)
                
            else:
                await game.process_command(command)
                
    except KeyboardInterrupt:
        console.print("\n[yellow]Game interrupted. Saving...[/yellow]")
        await game.save_game()
        console.print("[green]Game saved![/green]")
    except Exception as e:
        logger.error(f"Error in game loop: {e}")
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
