# Contributing to LLMAdventure 🎮

Thank you for your interest in contributing to LLMAdventure! We're excited to have you join our community of adventurers and developers.

## 🤝 How to Contribute

There are many ways to contribute to LLMAdventure:

- 🐛 **Report Bugs**: Help us identify and fix issues
- 💡 **Suggest Features**: Share your ideas for new features
- 📝 **Improve Documentation**: Help make our docs better
- 🔧 **Fix Issues**: Pick up a bug and fix it
- ✨ **Add Features**: Implement new functionality
- 🎨 **Design**: Help with UI/UX improvements
- 🧪 **Test**: Help ensure quality and stability
- 🌍 **Translate**: Help localize the game
- 📚 **Create Content**: Add new stories, quests, or plugins
- 🎮 **Play and Feedback**: Test the game and provide feedback

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- A Google AI API key (for testing)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/llmadventure.git
   cd llmadventure
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set Up Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Configure API Key**
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=llmadventure

# Run specific test categories
pytest -m "not slow"        # Skip slow tests
pytest -m integration       # Run integration tests
pytest -m unit             # Run unit tests

# Run tests in parallel
pytest -n auto

# Generate coverage report
pytest --cov=llmadventure --cov-report=html
```

### Writing Tests

- Follow the existing test structure
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Use fixtures for common setup

Example test:
```python
import pytest
from llmadventure.core.game import Game

@pytest.mark.asyncio
async def test_game_initialization():
    """Test that a new game initializes correctly."""
    game = Game()
    await game.initialize_new_game("TestPlayer", "warrior")
    
    assert game.player.name == "TestPlayer"
    assert game.player.player_class.value == "warrior"
    assert game.game_running is True
```

## 📝 Code Style

We use several tools to maintain code quality:

### Black (Code Formatting)
```bash
black llmadventure/
```

### isort (Import Sorting)
```bash
isort llmadventure/
```

### flake8 (Linting)
```bash
flake8 llmadventure/
```

### mypy (Type Checking)
```bash
mypy llmadventure/
```

### Pre-commit Hooks
We use pre-commit hooks to automatically run these tools:
```bash
pre-commit run --all-files
```

## 🔧 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run the full test suite
pytest

# Run linting and type checking
pre-commit run --all-files

# Test the game manually
python main.py
```

### 4. Submit a Pull Request

1. Push your branch to your fork
2. Create a pull request against the main branch
3. Fill out the PR template
4. Request review from maintainers

## 📋 Pull Request Guidelines

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] Manual testing completed
- [ ] No breaking changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: Maintainers review the code
3. **Testing**: Changes are tested in different environments
4. **Approval**: PR is approved and merged

## 🎯 Areas for Contribution

### High Priority
- 🐛 Bug fixes
- 📚 Documentation improvements
- 🧪 Test coverage
- 🚀 Performance optimizations

### Medium Priority
- ✨ New features
- 🎨 UI/UX improvements
- 🔧 Plugin system enhancements
- 🌐 Web interface improvements

### Low Priority
- 🎵 Sound effects
- 🎨 ASCII art
- 🌍 Localization
- 📊 Analytics features

## 🎮 Plugin Development

LLMAdventure uses a simple plugin system. To create a plugin, inherit from the `Plugin` base class and use the `register_plugin` decorator from `llmadventure.plugins`:

```python
from llmadventure.plugins import Plugin, register_plugin

@register_plugin
class MyPlugin(Plugin):
    name = "My Custom Plugin"
    version = "1.0.0"
    description = "A custom plugin for LLMAdventure"
    
    def on_game_start(self, game):
        # Plugin initialization
        pass
```

2. **Add Event Handlers**
   ```python
   def on_combat_start(self, player, enemy):
       # Custom combat mechanics
       pass
   
   def on_quest_complete(self, player, quest):
       # Custom rewards
       pass
   ```

3. **Test Your Plugin**
   ```bash
   pytest tests/test_plugins.py::test_my_plugin
   ```

## 📚 Documentation

### Writing Documentation

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep documentation up to date

### Documentation Structure

```
docs/
├── user-guide/          # User documentation
├── api/                 # API reference
├── plugins/             # Plugin development
├── tutorials/           # Step-by-step guides
└── contributing/        # This file
```

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Search documentation
3. Try to reproduce the issue
4. Check system requirements

### Bug Report Template

```markdown
## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- LLMAdventure: [e.g., 1.0.0]
- API Provider: [e.g., Google Gemini]

## Additional Information
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Before Requesting

1. Check if the feature already exists
2. Search existing issues
3. Consider if it fits the project scope
4. Think about implementation complexity

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why this feature is needed

## Proposed Implementation
How it could be implemented

## Alternatives Considered
Other approaches considered

## Additional Information
Mockups, examples, etc.
```

## 🏆 Recognition

Contributors are recognized in several ways:

- **Contributors List**: Added to README.md
- **Release Notes**: Mentioned in changelog
- **Hall of Fame**: Featured on our website
- **Swag**: LLMAdventure merchandise for significant contributions

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: [Bug reports and feature requests](https://github.com/SoftwareApkDev/llmadventure/issues)
- **GitHub Discussions**: [General discussion](https://github.com/SoftwareApkDev/llmadventure/discussions)
- **Email**: softwareapkdev2022@gmail.com

### Mentorship

New contributors can request mentorship:
- Request code reviews
- Get help with setup
- Learn best practices

## 📜 License

By contributing to LLMAdventure, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to LLMAdventure!** 🎮✨

Your contributions help make LLMAdventure better for everyone. We appreciate your time and effort!
