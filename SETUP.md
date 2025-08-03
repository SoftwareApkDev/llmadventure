# 🚀 LLMAdventure Setup Guide

Welcome to LLMAdventure! This guide will help you get up and running quickly.

## 📋 Prerequisites

- **Python 3.8+** (3.11+ recommended)
- **Google AI API Key** (for Gemini 2.5 Flash)
- **Git** (for development)
- **Docker** (optional, for containerized deployment)

## 🎯 Quick Start (5 minutes)

### 1. Install LLMAdventure

```bash
# Install from PyPI (recommended)
pip install llmadventure

# Or install with all features
pip install "llmadventure[full]"
```

### 2. Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your clipboard

### 3. Set Up Your API Key

```bash
# Option 1: Environment variable
export GOOGLE_API_KEY=your_api_key_here

# Option 2: .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 4. Start Your Adventure!

```bash
# Start the game
llmadventure

# Or use alternative commands
llm-adventure
adventure
```

**That's it!** You're ready to play! 🎮

## 🛠️ Advanced Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/SoftwareApkDev/llmadventure.git
cd llmadventure

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

### With Docker

```bash
# Pull the image
docker pull llmadventure/llmadventure:latest

# Run with Docker
docker run -it --rm \
  -e GOOGLE_API_KEY=your_api_key_here \
  -v $(pwd)/saves:/app/saves \
  llmadventure/llmadventure:latest
```

### With Docker Compose

```bash
# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Start services
docker-compose up -d

# Access web interface
open http://localhost:8001
```

## 🔧 Configuration

### Configuration File

Create `~/.config/llmadventure/config.yaml`:

```yaml
# API Configuration
api:
  provider: "google"
  model: "gemini-2.5-flash"
  timeout: 30
  retries: 3

# Game Settings
game:
  auto_save: true
  auto_save_interval: 300  # seconds
  difficulty: "normal"      # easy, normal, hard
  theme: "dark"            # light, dark, auto
  language: "en"           # en, es, fr, de, etc.

# UI Settings
ui:
  colors: true
  animations: true
  sound: false
  accessibility:
    high_contrast: false
    screen_reader: false

# Performance
performance:
  cache_enabled: true
  cache_ttl: 3600
  max_concurrent_requests: 5
  request_timeout: 30

# Logging
logging:
  level: "INFO"
  file: "/app/logs/llmadventure.log"
  max_size: "10MB"
  backup_count: 5
```

### Environment Variables

| Variable                 | Description       | Default                              |
|--------------------------|-------------------|--------------------------------------|
| `GOOGLE_API_KEY`         | Google AI API key | Required                             |
| `LLMADVENTURE_CONFIG`    | Config file path  | `~/.config/llmadventure/config.yaml` |
| `LLMADVENTURE_DATA_DIR`  | Data directory    | `~/.local/share/llmadventure`        |
| `LLMADVENTURE_LOG_LEVEL` | Log level         | `INFO`                               |
| `LLMADVENTURE_THEME`     | UI theme          | `auto`                               |
| `LLMADVENTURE_LANGUAGE`  | Language          | `en`                                 |

## 🎮 Game Modes

### CLI Mode (Default)

```bash
# Start CLI game
llmadventure

# With options
llmadventure --difficulty hard --theme light
```

### Web Interface

```bash
# Install web dependencies
pip install "llmadventure[web]"

# Start web server
llmadventure --web --host 0.0.0.0 --port 8000

# Or use Docker
docker run -p 8000:8000 llmadventure/llmadventure:web
```

### Development Mode

```bash
# Install development dependencies
pip install "llmadventure[dev]"

# Run tests
pytest

# Run with debugging
python -m pdb main.py
```

## 🔌 Plugin Development

### Creating a Plugin

LLMAdventure supports plugins via a simple base class and decorator. Place your plugin anywhere in your project, and import from `llmadventure.plugins`:

```python
from llmadventure.plugins import Plugin, register_plugin

@register_plugin
class MyPlugin(Plugin):
    name = "My Custom Plugin"
    version = "1.0.0"
    description = "A custom plugin for LLMAdventure"
    
    def on_game_start(self, game):
        print("🎉 My plugin is loaded!")
    
    def on_combat_start(self, player, enemy):
        print(f"⚔️ {player.name} vs {enemy.name}")
```

### Installing Plugins

```bash
# Copy plugin to plugins directory
cp my_plugin.py ~/.config/llmadventure/plugins/

# Or install via pip
pip install my-llmadventure-plugin
```

## 🧪 Testing

### Run Test Suite

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=llmadventure --cov-report=html

# Run specific tests
pytest tests/test_game.py -v

# Run performance tests
pytest tests/test_performance.py -m "not slow"
```

### Manual Testing

```bash
# Test CLI interface
llmadventure --test

# Test web interface
llmadventure --web --test

# Test API
python -m pytest tests/test_api.py
```

## 🚀 Deployment

### Production Deployment

```bash
# Using Docker
docker run -d \
  --name llmadventure \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -v /path/to/data:/app/data \
  llmadventure/llmadventure:latest

# Using Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment

#### Heroku

```bash
# Create Procfile
echo "web: llmadventure --web --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create my-llmadventure
heroku config:set GOOGLE_API_KEY=your_key
git push heroku main
```

#### AWS

```bash
# Using AWS ECS
aws ecs create-service \
  --cluster llmadventure \
  --service-name llmadventure \
  --task-definition llmadventure:1 \
  --desired-count 2
```

#### Google Cloud

```bash
# Deploy to Cloud Run
gcloud run deploy llmadventure \
  --image gcr.io/PROJECT_ID/llmadventure \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📊 Monitoring

### Health Checks

```bash
# Check service health
curl http://localhost:8000/health

# Check metrics
curl http://localhost:8000/metrics
```

### Logging

```bash
# View logs
tail -f /app/logs/llmadventure.log

# With Docker
docker logs -f llmadventure
```

### Metrics

```bash
# Prometheus metrics
curl http://localhost:8000/metrics

# Grafana dashboard
open http://localhost:3000
```

## 🔒 Security

### API Key Security

```bash
# Use environment variables (recommended)
export GOOGLE_API_KEY=your_key

# Use secrets management
echo $GOOGLE_API_KEY | docker secret create llmadventure_api_key -

# Use Kubernetes secrets
kubectl create secret generic llmadventure-secrets \
  --from-literal=google-api-key=your_key
```

### Network Security

```bash
# Use HTTPS
llmadventure --web --ssl-cert cert.pem --ssl-key key.pem

# Use reverse proxy
nginx -c /path/to/nginx.conf
```

## 🆘 Troubleshooting

### Common Issues

#### API Key Issues

```bash
# Check if API key is set
echo $GOOGLE_API_KEY

# Test API connection
python -c "import google.generativeai as genai; genai.configure(api_key='your_key')"
```

#### Installation Issues

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear cache
pip cache purge

# Reinstall
pip uninstall llmadventure
pip install llmadventure
```

#### Performance Issues

```bash
# Check system resources
htop

# Monitor API usage
curl http://localhost:8000/metrics

# Enable debug logging
export LLMADVENTURE_LOG_LEVEL=DEBUG
```

### Getting Help

- 📧 **Email**: softwareapkdev2022@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/SoftwareApkDev/llmadventure/issues)
- 📖 **Documentation**: [documentation](https://github.com/SoftwareApkDev/llmadventure/blob/master/README.md)

## 🎉 Next Steps

1. **Play the game**: Start your first adventure!
2. **Join the community**: Connect with other players
3. **Create plugins**: Extend the game with custom content
4. **Contribute**: Help improve LLMAdventure
5. **Share**: Tell others about your adventures

---

**Happy adventuring!** 🗡️⚔️🏰

For more information, visit [llmadventure.com](https://llmadventure.com)
