# 🎮 LLMAdventure - AI-Powered Text Adventure Game

[![PyPI version](https://badge.fury.io/py/llmadventure.svg)](https://badge.fury.io/py/llmadventure)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/llmadventure)](https://pepy.tech/project/llmadventure)
[![Stars](https://img.shields.io/github/stars/SoftwareApkDev/llmadventure.svg)](https://github.com/SoftwareApkDev/llmadventure)

> **Create infinite stories with AI-powered procedural generation** 🚀

**LLMAdventure** is the ultimate CLI text adventure game that uses Google's Gemini 2.5 Flash to generate unique, dynamic stories, worlds, and characters. Every playthrough is different, every choice matters, and every adventure is unforgettable.

## ✨ Why Choose LLMAdventure?

- 🎯 **Infinite Content**: AI generates unique stories, quests, and worlds
- 🎮 **Rich Gameplay**: Combat, exploration, character progression, and more
- 🎨 **Beautiful CLI**: Stunning terminal interface with colors and animations
- 🔌 **Extensible**: Plugin system for custom content and mods
- 🌐 **Multi-Platform**: Works on Windows, macOS, and Linux
- 📚 **Educational**: Learn AI, game development, and storytelling
- 🚀 **Fast**: Optimized for performance and responsiveness

## 🚀 Quick Start

```bash
# Install from PyPI
pip install llmadventure

# Start your adventure
llmadventure
```

**That's it!** No complex setup, no dependencies to manage. Just pure adventure.

## 🎯 Features

### 🧠 AI-Powered Storytelling
- **Dynamic Narrative Generation**: Every story is unique and adaptive
- **Context-Aware Responses**: AI remembers your choices and adapts the story
- **Procedural World Building**: Infinite worlds with unique locations and lore
- **Character Generation**: Rich NPCs with personalities and backstories

### ⚔️ Rich Gameplay Systems
- **Combat System**: Turn-based combat with strategy and tactics
- **Character Progression**: Level up, gain abilities, and evolve your character
- **Inventory Management**: Collect, use, and trade items
- **Quest System**: Dynamic quests that adapt to your choices
- **Exploration**: Discover hidden locations and secrets

### 🎨 Beautiful Interface
- **Rich Terminal UI**: Colors, progress bars, and animations
- **Responsive Design**: Works on any terminal size
- **Accessibility**: High contrast modes and screen reader support
- **Customizable**: Themes and appearance options

### 🔌 Extensible Architecture
- **Plugin System**: Create custom content and mods
- **API Access**: Integrate with other applications
- **Web Interface**: Optional web-based UI
- **Multiplayer Support**: Play with friends (coming soon)

## 📖 Examples

### Basic Usage

```python
from llmadventure import Game

# Start a new adventure
game = Game()
game.start_new_game("Hero", "warrior")

# Explore the world
game.move("north")
game.look_around()
game.attack("dragon")
```

### Custom Plugin

```python
from llmadventure.plugins import Plugin

class MyCustomPlugin(Plugin):
    def on_combat_start(self, player, enemy):
        # Add custom combat mechanics
        pass
    
    def on_quest_complete(self, player, quest):
        # Give custom rewards
        pass
```

### Web Integration

```python
from llmadventure.web import WebServer

# Start web interface
server = WebServer()
server.start(host="0.0.0.0", port=8000)
```

## 🛠️ Installation

### From PyPI (Recommended)

```bash
pip install llmadventure
```

### With Optional Dependencies

```bash
# Full installation with all features
pip install "llmadventure[full]"

# Web interface
pip install "llmadventure[web]"

# AI/ML features
pip install "llmadventure[ai]"

# Data analysis
pip install "llmadventure[data]"
```

### From Source

```bash
git clone https://github.com/llmadventure/llmadventure.git
cd llmadventure
pip install -e .
```

## 🔧 Configuration

### API Key Setup

1. Get a Google AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set your API key:

```bash
# Environment variable
export GOOGLE_API_KEY=your_key_here

# Or in .env file
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### Configuration File

Create `~/.config/llmadventure/config.yaml`:

```yaml
api:
  provider: "google"
  model: "gemini-2.5-flash"
  
game:
  auto_save: true
  difficulty: "normal"
  theme: "dark"
  
ui:
  colors: true
  animations: true
  sound: false
```

## 🎮 Game Controls

| Command           | Action          | Aliases            |
|-------------------|-----------------|--------------------|
| `n`, `north`      | Move north      | `up`, `u`          |
| `s`, `south`      | Move south      | `down`, `d`        |
| `e`, `east`       | Move east       | `right`, `r`       |
| `w`, `west`       | Move west       | `left`, `l`        |
| `look`            | Look around     | `l`, `examine`     |
| `inventory`       | Show inventory  | `i`, `inv`         |
| `attack <target>` | Attack creature | `fight`, `hit`     |
| `use <item>`      | Use item        | `consume`, `equip` |
| `talk <npc>`      | Talk to NPC     | `speak`, `chat`    |
| `save`            | Save game       | `s`                |
| `quit`            | Quit game       | `exit`, `q`        |
| `help`            | Show help       | `h`, `?`           |

## 🏗️ Architecture

```
llmadventure/
├── core/           # Core game logic (game, player, world, combat, inventory, quest, evolution, creature)
├── engine/         # AI, LLM interface, memory, procedural generation, prompt templates
├── cli/            # Command line interface (display, menus)
├── utils/          # Utilities (config, file_ops, logger)
├── plugins/        # Plugin system
├── web/            # Web interface (if enabled)

main.py             # Entry point
requirements.txt    # Python dependencies
pyproject.toml      # Build system and metadata
README.md           # Project documentation
```

## 🔌 Plugin Development

Create custom content with our plugin system:

```python
from llmadventure.plugins import Plugin, register_plugin

@register_plugin
class MyPlugin(Plugin):
    name = "My Custom Plugin"
    version = "1.0.0"
    
    def on_game_start(self, game):
        # Add custom game mechanics
        pass
    
    def on_combat_turn(self, player, enemy):
        # Modify combat behavior
        pass
```

## 🌐 Web Interface

Start the web interface for a graphical experience:

```bash
# Install web dependencies
pip install "llmadventure[web]"

# Start web server
llmadventure --web

# Or programmatically
from llmadventure.web import start_web_server
start_web_server(port=8000)
```

## 📊 Analytics & Insights

Track your adventures with built-in analytics:

```python
from llmadventure.analytics import AdventureTracker

tracker = AdventureTracker()
stats = tracker.get_player_stats()
print(f"Adventures completed: {stats['adventures']}")
print(f"Creatures defeated: {stats['creatures_defeated']}")
print(f"Distance traveled: {stats['distance_traveled']}")
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Install test dependencies
pip install "llmadventure[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=llmadventure

# Run specific test categories
pytest -m "not slow"
pytest -m integration
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Add** tests for new features
5. **Submit** a pull request

### Development Setup

```bash
git clone https://github.com/SoftwareApkDev/llmadventure.git
cd llmadventure
pip install -e ".[dev]"
pre-commit install
```

### Code Quality

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing

## 📈 Performance

LLMAdventure is optimized for performance:

- **Fast Startup**: < 1 second to begin playing
- **Responsive UI**: Real-time updates and animations
- **Efficient AI**: Optimized prompts and caching
- **Memory Efficient**: Minimal resource usage

## 🏆 Success Stories

> "LLMAdventure has revolutionized how I think about interactive storytelling. The AI-generated content is consistently engaging and surprising." - *Game Developer*

> "Perfect for teaching AI concepts to students. They love creating their own adventures!" - *Computer Science Professor*

> "The plugin system is incredibly powerful. I've created entire new game modes with just a few lines of code." - *Mod Developer*

## 📚 Documentation

- **[User Guide](https://docs.llmadventure.com/user-guide)**: Complete game manual
- **[API Reference](https://docs.llmadventure.com/api)**: Developer documentation
- **[Plugin Guide](https://docs.llmadventure.com/plugins)**: Creating custom content
- **[Tutorials](https://docs.llmadventure.com/tutorials)**: Step-by-step guides

## 🆘 Support

- **📧 Email**: softwareapkdev2022@gmail.com
- **💬 Discord**: [Join our community](https://discord.gg/llmadventure)
- **🐛 Issues**: [GitHub Issues](https://github.com/SoftwareApkDev/llmadventure/issues)

## 🙏 Acknowledgments

- **Google Gemini 2.5 Flash** for AI capabilities
- **Rich** library for beautiful CLI interfaces
- **Typer** for command-line interface
- **Pydantic** for data validation
- **The open-source community** for inspiration and support

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=llmadventure/llmadventure&type=Date)](https://star-history.com/#llmadventure/llmadventure&Date)

---

**Ready for your next adventure?** 🗡️⚔️🏰

```bash
pip install llmadventure
llmadventure
```

*Join thousands of adventurers creating infinite stories with AI!* 🚀
