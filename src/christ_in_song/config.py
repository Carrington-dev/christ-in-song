"""
Configuration management for Christ In Song application
"""
from pathlib import Path
from typing import Optional
import sys
import os


class Config:
    """Application configuration manager"""
    
    # Version
    VERSION = "1.0.0"
    
    # Application metadata
    APP_NAME = "Christ In Song"
    ORGANIZATION = "Christ In Song"
    
    # Database
    DATABASE_NAME = "christ_in_song.db"
    
    # UI Settings
    DEFAULT_WINDOW_WIDTH = 1000
    DEFAULT_WINDOW_HEIGHT = 700
    DEFAULT_FONT_SIZE = 12
    
    # Theme
    DEFAULT_THEME = "light"
    
    @staticmethod
    def get_user_data_dir() -> Path:
        """Get user data directory for the application"""
        if sys.platform == "win32":
            base_dir = Path(os.environ.get("APPDATA", Path.home()))
        elif sys.platform == "darwin":
            base_dir = Path.home() / "Library" / "Application Support"
        else:
            base_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        
        app_dir = base_dir / "ChristInSong"
        app_dir.mkdir(parents=True, exist_ok=True)
        return app_dir
    
    @staticmethod
    def get_database_path() -> Path:
        """Get path to the SQLite database"""
        return Config.get_user_data_dir() / Config.DATABASE_NAME
    
    @staticmethod
    def get_resource_path(relative_path: str) -> Path:
        """Get absolute path to resource file"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = Path(sys._MEIPASS)
        else:
            # Running in development
            base_path = Path(__file__).parent / "resources"
        
        return base_path / relative_path
    
    @staticmethod
    def get_backup_dir() -> Path:
        """Get backup directory path"""
        backup_dir = Config.get_user_data_dir() / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir
