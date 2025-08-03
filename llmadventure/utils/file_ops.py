"""
File operations utilities for LLMAdventure
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from ..utils.logger import logger

class FileOps:
    """File operations utility class"""
    
    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> Path:
        """Ensure directory exists, create if it doesn't"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: Union[str, Path], indent: int = 2) -> bool:
        """Save data to JSON file"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            
            logger.debug(f"Saved JSON file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving JSON file {file_path}: {e}")
            return False
    
    @staticmethod
    def load_json(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"JSON file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.debug(f"Loaded JSON file: {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {e}")
            return None
    
    @staticmethod
    def save_yaml(data: Dict[str, Any], file_path: Union[str, Path]) -> bool:
        """Save data to YAML file"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            logger.debug(f"Saved YAML file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving YAML file {file_path}: {e}")
            return False
    
    @staticmethod
    def load_yaml(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """Load data from YAML file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"YAML file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            logger.debug(f"Loaded YAML file: {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading YAML file {file_path}: {e}")
            return None
    
    @staticmethod
    def list_files(directory: Union[str, Path], pattern: str = "*") -> List[Path]:
        """List files in directory matching pattern"""
        try:
            directory = Path(directory)
            
            if not directory.exists():
                logger.warning(f"Directory not found: {directory}")
                return []
            
            files = list(directory.glob(pattern))
            logger.debug(f"Found {len(files)} files in {directory} matching {pattern}")
            return files
            
        except Exception as e:
            logger.error(f"Error listing files in {directory}: {e}")
            return []
    
    @staticmethod
    def copy_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Copy file from source to destination"""
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                logger.error(f"Source file not found: {source}")
                return False
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copy2(source, destination)
            
            logger.debug(f"Copied file from {source} to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Error copying file from {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def move_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Move file from source to destination"""
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                logger.error(f"Source file not found: {source}")
                return False
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.move(str(source), str(destination))
            
            logger.debug(f"Moved file from {source} to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Error moving file from {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def delete_file(file_path: Union[str, Path]) -> bool:
        """Delete file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"File not found for deletion: {file_path}")
                return False
            
            file_path.unlink()
            
            logger.debug(f"Deleted file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    @staticmethod
    def get_file_size(file_path: Union[str, Path]) -> Optional[int]:
        """Get file size in bytes"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                return None
            
            size = file_path.stat().st_size
            logger.debug(f"File size of {file_path}: {size} bytes")
            return size
            
        except Exception as e:
            logger.error(f"Error getting file size of {file_path}: {e}")
            return None
    
    @staticmethod
    def get_file_modified_time(file_path: Union[str, Path]) -> Optional[float]:
        """Get file modification time"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                return None
            
            mtime = file_path.stat().st_mtime
            logger.debug(f"File modification time of {file_path}: {mtime}")
            return mtime
            
        except Exception as e:
            logger.error(f"Error getting file modification time of {file_path}: {e}")
            return None
    
    @staticmethod
    def backup_file(file_path: Union[str, Path], backup_suffix: str = ".backup") -> bool:
        """Create backup of file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"File not found for backup: {file_path}")
                return False
            
            backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
            
            import shutil
            shutil.copy2(file_path, backup_path)
            
            logger.debug(f"Created backup of {file_path} as {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating backup of {file_path}: {e}")
            return False
    
    @staticmethod
    def read_text_file(file_path: Union[str, Path]) -> Optional[str]:
        """Read text file content"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                logger.warning(f"Text file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.debug(f"Read text file: {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            return None
    
    @staticmethod
    def write_text_file(file_path: Union[str, Path], content: str) -> bool:
        """Write content to text file"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.debug(f"Wrote text file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing text file {file_path}: {e}")
            return False 