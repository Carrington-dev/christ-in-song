"""
Main application entry point for Christ In Song Hymnal
"""
import sys
import logging
from pathlib import Path

# PySide6 imports
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from christ_in_song.config import Config
from christ_in_song.database.connection import DatabaseManager
from christ_in_song.ui.main_window import MainWindow


def setup_logging() -> None:
    """Configure application logging"""
    log_dir = Config.get_user_data_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "christ_in_song.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main() -> int:
    """Main application function"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Christ In Song Hymnal v%s", Config.VERSION)
    
    try:
        # Create Qt Application
        app = QApplication(sys.argv)
        app.setApplicationName("Christ In Song")
        app.setApplicationVersion(Config.VERSION)
        app.setOrganizationName("Christ In Song")
        
        # Set application icon
        icon_path = Config.get_resource_path("icons/app_icon.ico")
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
        
        # Enable high DPI scaling
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Initialize database
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        logger.info("Application started successfully")
        
        # Run application event loop
        return app.exec()
        
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())