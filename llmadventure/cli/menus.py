"""
Menu system for LLMAdventure
"""

import asyncio
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm

from .display import DisplayManager
from ..utils.config import Config


class MenuSystem:
    """Menu system for handling different game menus"""
    
    def __init__(self, display: DisplayManager):
        self.display = display
        self.console = Console()
    
    async def show_main_menu(self) -> str:
        """Show main menu and get user choice"""
        while True:
            self.console.clear()

            menu_text = Text()
            menu_text.append("LLM", style="bold blue")
            menu_text.append("Adventure", style="bold green")
            menu_text.append("\n\n", style="default")
            menu_text.append("A CLI-based text adventure game powered by Gemini 2.5 Flash\n\n", style="italic")
            
            menu_text.append("1. ", style="bold")
            menu_text.append("New Game\n", style="cyan")
            menu_text.append("2. ", style="bold")
            menu_text.append("Load Game\n", style="cyan")
            menu_text.append("3. ", style="bold")
            menu_text.append("Settings\n", style="cyan")
            menu_text.append("4. ", style="bold")
            menu_text.append("Help\n", style="cyan")
            menu_text.append("5. ", style="bold")
            menu_text.append("Quit\n\n", style="cyan")
            
            menu_text.append("Select an option (1-5): ", style="yellow")
            
            panel = Panel(menu_text, title="[bold]Main Menu[/bold]", border_style="blue")
            self.console.print(panel)
            
            choice = Prompt.ask("", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                return "new_game"
            elif choice == "2":
                return "load_game"
            elif choice == "3":
                return "settings"
            elif choice == "4":
                return "help"
            elif choice == "5":
                return "quit"
    
    async def show_settings_menu(self, config: Config):
        """Show settings menu"""
        while True:
            self.console.clear()

            current_settings = {
                "API Key": "Set" if config.get_api_key() else "Not Set",
                "Model": config.get("model", "gemini-2.5-flash"),
                "Max Tokens": config.get("max_tokens", 2048),
                "Temperature": config.get("temperature", 0.7),
                "Auto Save": "Enabled" if config.get("save_auto", True) else "Disabled",
                "Save Interval": f"{config.get('save_interval', 5)} minutes",
                "Debug Mode": "Enabled" if config.get("debug_mode", False) else "Disabled",
                "Log Level": config.get("log_level", "INFO")
            }

            table = Table(title="[bold]Settings[/bold]")
            table.add_column("Setting", style="cyan")
            table.add_column("Current Value", style="green")
            
            for setting, value in current_settings.items():
                table.add_row(setting, str(value))
            
            self.console.print(table)

            menu_text = Text()
            menu_text.append("\n1. ", style="bold")
            menu_text.append("Set API Key\n", style="cyan")
            menu_text.append("2. ", style="bold")
            menu_text.append("Change Model\n", style="cyan")
            menu_text.append("3. ", style="bold")
            menu_text.append("Adjust Temperature\n", style="cyan")
            menu_text.append("4. ", style="bold")
            menu_text.append("Toggle Auto Save\n", style="cyan")
            menu_text.append("5. ", style="bold")
            menu_text.append("Toggle Debug Mode\n", style="cyan")
            menu_text.append("6. ", style="bold")
            menu_text.append("Back to Main Menu\n\n", style="cyan")
            
            menu_text.append("Select an option (1-6): ", style="yellow")
            
            panel = Panel(menu_text, title="[bold]Settings Menu[/bold]", border_style="green")
            self.console.print(panel)
            
            choice = Prompt.ask("", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                await self._set_api_key(config)
            elif choice == "2":
                await self._change_model(config)
            elif choice == "3":
                await self._adjust_temperature(config)
            elif choice == "4":
                await self._toggle_auto_save(config)
            elif choice == "5":
                await self._toggle_debug_mode(config)
            elif choice == "6":
                break
    
    async def _set_api_key(self, config: Config):
        """Set API key"""
        self.console.print("\n[bold]Set Google API Key[/bold]")
        self.console.print("Get your API key from: https://makersuite.google.com/app/apikey\n")
        
        api_key = Prompt.ask("Enter your Google API key", password=True)
        if api_key:
            config.set_api_key(api_key)
            self.console.print("[green]API key set successfully![/green]")
        else:
            self.console.print("[yellow]No API key entered.[/yellow]")
        
        await asyncio.sleep(2)
    
    async def _change_model(self, config: Config):
        """Change LLM model"""
        self.console.print("\n[bold]Change LLM Model[/bold]")
        self.console.print("Available models:\n")
        self.console.print("1. gemini-2.5-flash (Recommended)")
        self.console.print("2. gemini-2.0-flash")
        self.console.print("3. gemini-2.0-pro")
        
        choice = Prompt.ask("Select model (1-3)", choices=["1", "2", "3"])
        
        models = {
            "1": "gemini-2.5-flash",
            "2": "gemini-2.0-flash",
            "3": "gemini-2.0-pro"
        }
        
        config.set("model", models[choice])
        self.console.print(f"[green]Model changed to {models[choice]}![/green]")
        await asyncio.sleep(2)
    
    async def _adjust_temperature(self, config: Config):
        """Adjust temperature setting"""
        self.console.print("\n[bold]Adjust Temperature[/bold]")
        self.console.print("Temperature controls creativity (0.0 = focused, 1.0 = creative)\n")
        
        current_temp = config.get("temperature", 0.7)
        self.console.print(f"Current temperature: {current_temp}")
        
        try:
            new_temp = float(Prompt.ask("Enter new temperature (0.0-1.0)"))
            if 0.0 <= new_temp <= 1.0:
                config.set("temperature", new_temp)
                self.console.print(f"[green]Temperature set to {new_temp}![/green]")
            else:
                self.console.print("[red]Temperature must be between 0.0 and 1.0[/red]")
        except ValueError:
            self.console.print("[red]Invalid temperature value[/red]")
        
        await asyncio.sleep(2)
    
    async def _toggle_auto_save(self, config: Config):
        """Toggle auto save setting"""
        current = config.get("save_auto", True)
        new_value = not current
        
        config.set("save_auto", new_value)
        status = "enabled" if new_value else "disabled"
        self.console.print(f"[green]Auto save {status}![/green]")
        
        await asyncio.sleep(2)
    
    async def _toggle_debug_mode(self, config: Config):
        """Toggle debug mode"""
        current = config.get("debug_mode", False)
        new_value = not current
        
        config.set("debug_mode", new_value)
        status = "enabled" if new_value else "disabled"
        self.console.print(f"[green]Debug mode {status}![/green]")
        
        await asyncio.sleep(2)
    
    async def show_help(self):
        """Show help menu"""
        self.console.clear()
        
        help_text = """
[bold]LLMAdventure - Help & Information[/bold]

[bold blue]About the Game[/bold blue]
LLMAdventure is a CLI-based text adventure game powered by Google's Gemini 2.5 Flash model.
The game features procedurally generated worlds, dynamic storytelling, and AI-driven content.

[bold green]Key Features[/bold green]
• AI-powered storytelling with Gemini 2.5 Flash
• Procedural world generation
• Dynamic creature encounters
• Quest system with multiple objectives
• Character progression and evolution
• Rich CLI interface with colors and formatting
• Save/load system for persistent gameplay

[bold yellow]Getting Started[/bold yellow]
1. Set up your Google API key in Settings
2. Create a new character (Warrior, Mage, Rogue, or Ranger)
3. Explore the world using movement commands
4. Interact with NPCs and complete quests
5. Battle creatures and collect loot
6. Level up and develop your character

[bold magenta]Tips for Success[/bold magenta]
• Use 'look' frequently to get detailed descriptions
• Talk to NPCs to learn about quests and lore
• Save your game regularly
• Pay attention to creature behaviors
• Experiment with different character classes
• Explore thoroughly to find hidden content

[bold cyan]Technical Information[/bold cyan]
• Built with Python 3.8+
• Uses Rich library for CLI formatting
• Integrates with Google Generative AI
• Supports custom plugins and mods
• Cross-platform compatibility

[bold red]Troubleshooting[/bold red]
• Ensure your API key is valid and has sufficient quota
• Check your internet connection for LLM requests
• Verify Python version compatibility
• Check logs for detailed error information
        """
        
        panel = Panel(help_text, title="[bold]Help & Information[/bold]", border_style="blue")
        self.console.print(panel)
        
        Prompt.ask("\nPress Enter to continue")
    
    async def show_character_creation(self) -> Dict[str, str]:
        """Show character creation menu"""
        self.console.clear()

        self.console.print("[bold blue]Character Creation[/bold blue]\n")
        name = Prompt.ask("Enter your character's name")
        if not name:
            name = "Adventurer"

        self.console.print("\n[bold]Choose your character class:[/bold]\n")
        
        classes = [
            ("Warrior", "High health and attack, excels in melee combat"),
            ("Mage", "High mana and intelligence, powerful magic abilities"),
            ("Rogue", "High speed and stealth, excels at sneaking and ranged combat"),
            ("Ranger", "Balanced stats, skilled with bows and survival")
        ]
        
        for i, (class_name, description) in enumerate(classes, 1):
            self.console.print(f"{i}. [bold]{class_name}[/bold] - {description}")
        
        choice = Prompt.ask("\nSelect your class", choices=["1", "2", "3", "4"])
        player_class = classes[int(choice) - 1][0].lower()
        
        return {
            "name": name,
            "class": player_class
        }
    
    async def show_save_selection(self, save_files: list) -> Optional[str]:
        """Show save file selection menu"""
        if not save_files:
            self.console.print("[yellow]No save files found.[/yellow]")
            await asyncio.sleep(2)
            return None
        
        self.console.clear()
        self.console.print("[bold blue]Load Game[/bold blue]\n")
        self.console.print("[bold]Available save files:[/bold]\n")
        
        for i, save_file in enumerate(save_files, 1):
            self.console.print(f"{i}. {save_file.stem}")
        
        choice = Prompt.ask(f"\nSelect save file (1-{len(save_files)})", 
                           choices=[str(i) for i in range(1, len(save_files) + 1)])
        
        selected_file = save_files[int(choice) - 1]
        return str(selected_file)
    
    async def show_confirmation(self, message: str) -> bool:
        """Show confirmation dialog"""
        return Confirm.ask(message)
    
    async def show_error(self, error_message: str):
        """Show error message"""
        panel = Panel(error_message, title="[bold red]Error[/bold red]", border_style="red")
        self.console.print(panel)
        await asyncio.sleep(3)
    
    async def show_success(self, message: str):
        """Show success message"""
        panel = Panel(message, title="[bold green]Success[/bold green]", border_style="green")
        self.console.print(panel)
        await asyncio.sleep(2)
