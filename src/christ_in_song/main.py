"""
Main application entry point for Christ In Song Hymnal
File: src/christ_in_song/main.py
"""
import sys
import logging
from pathlib import Path

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMessageBox
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
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )


def show_error_dialog(title: str, message: str) -> None:
    """Show an error dialog to the user"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()


def main() -> int:
    """Main application function"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("=" * 70)
    logger.info("Starting Christ In Song Hymnal v%s", Config.VERSION)
    logger.info("=" * 70)

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

        logger.info("Initializing database...")
        print("\n🔄 Initializing database...\n")

        # Initialize database
        db_manager = DatabaseManager()
        if not db_manager.initialize_database():
            error_msg = (
                "Failed to initialize the database.\n\n"
                "Please check the log file for details:\n"
                f"{Config.get_user_data_dir() / 'logs' / 'christ_in_song.log'}"
            )
            logger.error("Database initialization failed")
            show_error_dialog("Database Error", error_msg)
            return 1

        logger.info("Database initialized successfully")
        print("✅ Database initialized successfully!\n")

        # Show database stats
        stats = db_manager.get_database_stats()
        logger.info("Database statistics:")
        logger.info("  Total hymns: %d", stats["total_hymns"])
        logger.info("  Total categories: %d", stats["total_categories"])
        logger.info("  Total favorites: %d", stats["total_favorites"])
        logger.info("  Database size: %d bytes", stats["database_size"])

        print("📊 Database Statistics:")
        print(f"  • Total hymns: {stats['total_hymns']}")
        print(f"  • Total categories: {stats['total_categories']}")
        print(f"  • Total favorites: {stats['total_favorites']}")
        print(f"  • Database location: {db_manager.db_path}")
        print()

        # Create and show main window - PASS db_manager HERE
        logger.info("Creating main window...")
        main_window = MainWindow(db_manager)  # ← THIS IS THE CRITICAL LINE
        main_window.show()

        logger.info("Application started successfully")
        print("🎵 Christ In Song Hymnal is now running!\n")
        print("=" * 70)

        # Run application event loop
        return_code = app.exec()

        logger.info("Application exiting with code: %d", return_code)
        return return_code

    except Exception as e:
        logger.exception("Fatal error: %s", e)
        error_msg = (
            f"A fatal error occurred:\n\n{str(e)}\n\n"
            "Please check the log file for details:\n"
            f"{Config.get_user_data_dir() / 'logs' / 'christ_in_song.log'}"
        )
        show_error_dialog("Fatal Error", error_msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())