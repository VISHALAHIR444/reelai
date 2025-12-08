"""Utility functions and helpers"""

import logging
import json
from pathlib import Path
from app.core.config import get_settings

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)


def validate_youtube_url(url: str) -> bool:
    """Validate if URL is a valid YouTube URL"""
    try:
        valid_hosts = ["youtube.com", "youtu.be", "www.youtube.com"]
        return any(host in url for host in valid_hosts)
    except:
        return False


def create_directories(paths: list) -> bool:
    """Create multiple directories"""
    try:
        for path in paths:
            Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        get_logger(__name__).error(f"Error creating directories: {str(e)}")
        return False


def save_json(data: dict, filepath: str) -> bool:
    """Save data as JSON file"""
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        get_logger(__name__).error(f"Error saving JSON: {str(e)}")
        return False


def load_json(filepath: str) -> dict:
    """Load data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        get_logger(__name__).error(f"Error loading JSON: {str(e)}")
        return {}
