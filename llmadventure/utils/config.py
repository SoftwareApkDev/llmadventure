"""
Configuration management for LLMAdventure
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class Config:
    """Configuration manager for LLMAdventure"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config = {}
        self._load_config()
        
    def _get_default_config_path(self) -> str:
        """Get the default configuration file path"""
        config_dir = Path.home() / ".llmadventure"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.json")
    
    def _load_config(self):
        """Load configuration from file and environment"""
        load_dotenv()

        self._config = {
            "api_key": os.environ['GOOGLE_API_KEY'],
            "model": "gemini-2.5-flash",
            "max_tokens": 2048,
            "temperature": 0.7,
            "save_auto": True,
            "save_interval": 5,
            "ui_theme": "default",
            "sound_enabled": False,
            "debug_mode": False,
            "log_level": "INFO",
            "data_dir": str(Path.home() / ".llmadventure" / "data"),
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value"""
        self._config[key] = value
        self.save_config()
    
    def get_api_key(self) -> str:
        """Get the Google API key"""
        return self.get("api_key", "")
    
    def set_api_key(self, api_key: str):
        """Set the Google API key"""
        self.set("api_key", api_key)
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration"""
        return {
            "model": self.get("model"),
            "max_tokens": self.get("max_tokens"),
            "temperature": self.get("temperature"),
        }
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled"""
        return self.get("debug_mode", False)
    
    def get_data_dir(self) -> str:
        """Get the data directory path"""
        data_dir = self.get("data_dir")
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        return data_dir
