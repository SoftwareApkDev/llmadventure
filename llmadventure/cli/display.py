"""
Display manager for rich CLI output in LLMAdventure
"""

import asyncio
from typing import Dict, List, Any

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from ..core.combat import Combat
from ..core.creature import Creature
from ..core.player import Player
from ..core.world import Location
from ..utils.logger import logger


class DisplayManager:
    """Manages rich CLI display and UI rendering"""
    
    def __init__(self):
        self.console = Console()
        
    async def show_game_state(self, game):
        """Display current game state"""
        try:
            layout = Layout()

            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main"),
                Layout(name="footer", size=3)
            )

            layout["header"].update(self._create_header(game.player))
            layout["main"].update(self._create_main_content(game))
            layout["footer"].update(self._create_footer())

            self.console.clear()
            self.console.print(layout)
            
        except Exception as e:
            logger.error(f"Error displaying game state: {e}")
            self.console.print(f"[red]Error displaying game state: {e}[/red]")

    def _create_header(self, player: Player) -> Panel:
        """Create header panel with player information"""
        header_text = Text()
        header_text.append(f"{player.name} ", style="bold blue")
        header_text.append(f"Level {player.level} {player.player_class.value.title()}", style="green")
        header_text.append(f" | Health: {player.stats.health}/{player.stats.max_health}", style="red")
        header_text.append(f" | Mana: {player.stats.mana}/{player.stats.max_mana}", style="cyan")
        header_text.append(f" | Gold: {player.gold}", style="yellow")
        header_text.append(f" | Rep: {player.reputation}", style="magenta")
        
        return Panel(header_text, title="[bold]Character Status[/bold]", border_style="blue")
    
    def _create_main_content(self, game) -> Panel:
        """Create main content area"""
        content = []

        if game.current_location:
            location_info = self._create_location_info(game.current_location)
            content.append(location_info)

        if game.creatures_at_location:
            creatures_info = self._create_creatures_info(game.creatures_at_location)
            content.append(creatures_info)

        if game.items_at_location:
            items_info = self._create_items_info(game.items_at_location)
            content.append(items_info)

        if game.quests_available:
            quests_info = self._create_quests_info(game.quests_available)
            content.append(quests_info)
        
        if not content:
            content.append("[dim]Nothing notable here...[/dim]")
        
        return Panel("\n\n".join(content), title="[bold]Current Location[/bold]", border_style="green")
    
    def _create_location_info(self, location: Location) -> str:
        """Create location information display"""
        info = f"[bold]{location.name}[/bold]\n"
        info += f"[dim]{location.description}[/dim]\n"
        info += f"Biome: [cyan]{location.biome}[/cyan] | Difficulty: [red]{location.difficulty}[/red]\n"
        
        if location.features:
            features_text = ", ".join(location.features)
            info += f"Features: [yellow]{features_text}[/yellow]"
        
        return info
    
    def _create_creatures_info(self, creatures: List[Creature]) -> str:
        """Create creatures information display"""
        if not creatures:
            return ""
        
        info = "[bold red]Creatures here:[/bold red]\n"
        
        for creature in creatures:
            health_bar = self._create_health_bar(creature.stats.health, creature.stats.max_health)
            info += f"• [bold]{creature.name}[/bold] ({creature.creature_type.value}) {health_bar}\n"
        
        return info
    
    def _create_items_info(self, items: List[Dict[str, Any]]) -> str:
        """Create items information display"""
        if not items:
            return ""
        
        info = "[bold yellow]Items here:[/bold yellow]\n"
        
        for item in items:
            item_type = item.get("type", "unknown")
            info += f"• [bold]{item['name']}[/bold] ({item_type})\n"
        
        return info
    
    def _create_quests_info(self, quests: List) -> str:
        """Create quests information display"""
        if not quests:
            return ""
        
        info = "[bold magenta]Quests available:[/bold magenta]\n"
        
        for quest in quests:
            info += f"• [bold]{quest.title}[/bold] - {quest.description[:50]}...\n"
        
        return info
    
    def _create_footer(self) -> Panel:
        """Create footer with controls"""
        controls = [
            "[bold]Movement:[/bold] n/s/e/w",
            "[bold]Actions:[/bold] look/inventory/attack/talk",
            "[bold]System:[/bold] save/load/quit/help"
        ]
        
        return Panel(" | ".join(controls), title="[bold]Controls[/bold]", border_style="dim")
    
    def _create_health_bar(self, current: int, maximum: int) -> str:
        """Create a health bar display"""
        percentage = (current / maximum) * 100
        filled = int(percentage / 10)
        empty = 10 - filled
        
        bar = "█" * filled + "░" * empty
        color = "green" if percentage > 50 else "yellow" if percentage > 25 else "red"
        
        return f"[{color}]{bar}[/{color}] {current}/{maximum}"
    
    async def show_location_description(self, description: str, location: Location):
        """Show detailed location description"""
        panel = Panel(
            description,
            title=f"[bold]Exploring {location.name}[/bold]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    async def show_inventory(self, player: Player):
        """Show player inventory"""
        table = Table(title=f"[bold]Inventory - {player.name}[/bold]")
        table.add_column("Item", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Value", justify="right", style="green")
        table.add_column("Equipped", justify="center", style="yellow")
        
        for item in player.inventory:
            equipped = "✓" if item.get("equipped", False) else ""
            table.add_row(
                item["name"],
                item.get("type", "unknown"),
                str(item.get("value", 0)),
                equipped
            )
        
        self.console.print(table)
    
    async def show_player_status(self, player: Player):
        """Show detailed player status"""
        stats_table = Table(title=f"[bold]Character Stats - {player.name}[/bold]")
        stats_table.add_column("Stat", style="cyan")
        stats_table.add_column("Value", style="green")
        stats_table.add_column("Max", style="yellow")
        
        stats_table.add_row("Health", str(player.stats.health), str(player.stats.max_health))
        stats_table.add_row("Mana", str(player.stats.mana), str(player.stats.max_mana))
        stats_table.add_row("Attack", str(player.stats.attack), "")
        stats_table.add_row("Defense", str(player.stats.defense), "")
        stats_table.add_row("Speed", str(player.stats.speed), "")
        stats_table.add_row("Intelligence", str(player.stats.intelligence), "")
        stats_table.add_row("Charisma", str(player.stats.charisma), "")
        stats_table.add_row("Luck", str(player.stats.luck), "")

        skills_table = Table(title="[bold]Skills[/bold]")
        skills_table.add_column("Skill", style="cyan")
        skills_table.add_column("Level", style="green")
        
        skills_table.add_row("Sword Mastery", str(player.skills.sword_mastery))
        skills_table.add_row("Magic Mastery", str(player.skills.magic_mastery))
        skills_table.add_row("Stealth", str(player.skills.stealth))
        skills_table.add_row("Archery", str(player.skills.archery))
        skills_table.add_row("Healing", str(player.skills.healing))
        skills_table.add_row("Persuasion", str(player.skills.persuasion))

        exp_percentage = (player.experience / player.experience_to_next) * 100
        exp_bar = self._create_progress_bar(exp_percentage, 20)
        
        exp_text = f"Experience: {player.experience}/{player.experience_to_next} ({exp_percentage:.1f}%)"
        
        self.console.print(stats_table)
        self.console.print(skills_table)
        self.console.print(f"\n[bold]Level {player.level}[/bold] {exp_bar}")
        self.console.print(f"[dim]{exp_text}[/dim]")
    
    def _create_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Create a progress bar"""
        filled = int((percentage / 100) * width)
        empty = width - filled
        
        bar = "█" * filled + "░" * empty
        return f"[green]{bar}[/green]"
    
    async def show_combat_status(self, combat: Combat):
        """Show combat status"""
        status = combat.get_combat_status()
        
        if status["state"] == "inactive":
            return

        header = f"[bold red]Combat Round {status['round']}[/bold red]"

        player = status["player"]
        player_bar = self._create_health_bar(player["health"], player["max_health"])
        player_text = f"[blue]{player['name']}[/blue] {player_bar}"

        creature = status["creature"]
        creature_bar = self._create_health_bar(creature["health"], creature["max_health"])
        creature_text = f"[red]{creature['name']}[/red] {creature_bar}"

        actions_text = ""
        if status["recent_actions"]:
            actions_text = "\n[bold]Recent Actions:[/bold]\n"
            for action in status["recent_actions"]:
                actions_text += f"• {action['attacker']} attacks {action['target']} for {action['damage']} damage\n"
        
        panel = Panel(
            f"{player_text}\n{creature_text}{actions_text}",
            title=header,
            border_style="red"
        )
        
        self.console.print(panel)
    
    async def show_dialogue(self, npc_name: str, response: str):
        """Show NPC dialogue"""
        panel = Panel(
            response,
            title=f"[bold]Dialogue with {npc_name}[/bold]",
            border_style="cyan"
        )
        self.console.print(panel)
    
    async def show_help(self):
        """Show help information"""
        help_text = """
[bold]LLMAdventure - Help[/bold]

[bold blue]Movement Commands:[/bold blue]
• n, north - Move north
• s, south - Move south  
• e, east - Move east
• w, west - Move west

[bold green]Action Commands:[/bold green]
• look, l - Look around and get description
• inventory, i, inv - Show inventory
• status, stats, st - Show character status
• attack [creature] - Attack a creature
• talk [npc] - Talk to an NPC
• use [item] - Use an item from inventory
• take [item] - Take an item from location

[bold yellow]System Commands:[/bold yellow]
• save, s - Save the game
• load - Load a saved game
• quit, exit, q - Quit the game
• help, h, ? - Show this help

[bold magenta]Combat Commands:[/bold magenta]
• attack - Attack the current target
• defend - Defend against attacks
• use [item] - Use an item in combat
• flee - Try to escape from combat

[bold cyan]Tips:[/bold cyan]
• Type 'look' to get detailed descriptions of your surroundings
• Talk to NPCs to learn about quests and the world
• Save frequently to avoid losing progress
• Pay attention to creature behaviors and stats
        """
        
        panel = Panel(help_text, title="[bold]Help[/bold]", border_style="blue")
        self.console.print(panel)
    
    async def show_loading_screen(self, message: str = "Loading..."):
        """Show loading screen with spinner"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(message, total=None)
            await asyncio.sleep(0.1)
    
    async def show_message(self, message: str, message_type: str = "info"):
        """Show a message with appropriate styling"""
        colors = {
            "info": "blue",
            "success": "green", 
            "warning": "yellow",
            "error": "red"
        }
        
        color = colors.get(message_type, "white")
        panel = Panel(message, border_style=color)
        self.console.print(panel)
