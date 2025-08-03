"""
Logging utilities for LLMAdventure
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

class Logger:
    """Enhanced logger for LLMAdventure"""
    
    def __init__(self, name: str = "llmadventure", level: str = "INFO"):
        self.name = name
        self.level = getattr(logging, level.upper())
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with rich formatting"""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Console handler with rich formatting
        console = Console()
        console_handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True
        )
        console_handler.setLevel(self.level)
        logger.addHandler(console_handler)
        
        # File handler for persistent logs
        log_dir = Path.home() / ".llmadventure" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "llmadventure.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def game_event(self, event: str, details: Optional[dict] = None):
        """Log game-specific events"""
        if details:
            self.info(f"[GAME] {event}: {details}")
        else:
            self.info(f"[GAME] {event}")
    
    def combat_event(self, event: str, details: Optional[dict] = None):
        """Log combat-specific events"""
        if details:
            self.info(f"[COMBAT] {event}: {details}")
        else:
            self.info(f"[COMBAT] {event}")
    
    def ai_event(self, event: str, details: Optional[dict] = None):
        """Log AI-specific events"""
        if details:
            self.debug(f"[AI] {event}: {details}")
        else:
            self.debug(f"[AI] {event}")

# Global logger instance
logger = Logger() 