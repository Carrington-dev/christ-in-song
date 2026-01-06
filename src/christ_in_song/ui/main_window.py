"""
Main application window with database integration
File: src/christ_in_song/ui/main_window.py
"""
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QLineEdit,
    QTabWidget,
    QMessageBox,
    QSplitter,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from christ_in_song.config import Config
from christ_in_song.database.connection import DatabaseManager


class MainWindow(QMainWindow):
    """Main application window with database integration"""

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.current_hymn = None
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.VERSION}")
        self.setGeometry(100, 100, Config.DEFAULT_WINDOW_WIDTH, Config.DEFAULT_WINDOW_HEIGHT)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Add header
        header = self.create_header()
        main_layout.addWidget(header)

        # Add search bar
        search_layout = self.create_search_bar()
        main_layout.addLayout(search_layout)

        # Create splitter for hymn list and display
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Tabs for different views
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel - Hymn display
        self.hymn_display = self.create_hymn_display()
        splitter.addWidget(self.hymn_display)

        # Set initial sizes (30% left, 70% right)
        splitter.setSizes([300, 700])

        main_layout.addWidget(splitter)

        # Add status bar
        self.statusBar().showMessage("Ready")

    def create_header(self) -> QWidget:
        """Create header with title and stats"""
        header = QWidget()
        layout = QHBoxLayout()
        header.setLayout(layout)

        # Title
        title = QLabel("🎵 Christ In Song Hymnal")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
        """)
        layout.addWidget(title)

        layout.addStretch()

        # Stats label
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                padding: 10px;
            }
        """)
        layout.addWidget(self.stats_label)

        return header

    def create_search_bar(self) -> QHBoxLayout:
        """Create search bar"""
        layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search hymns by title, lyrics, author...")
        self.search_input.textChanged.connect(self.on_search)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.search_input)

        return layout

    def create_left_panel(self) -> QTabWidget:
        """Create left panel with tabs"""
        tabs = QTabWidget()

        # All Hymns tab
        self.hymns_list = QListWidget()
        self.hymns_list.itemClicked.connect(self.on_hymn_selected)
        tabs.addTab(self.hymns_list, "All Hymns")

        # Favorites tab
        self.favorites_list = QListWidget()
        self.favorites_list.itemClicked.connect(self.on_favorite_selected)
        tabs.addTab(self.favorites_list, "⭐ Favorites")

        # Recent tab
        self.recent_list = QListWidget()
        self.recent_list.itemClicked.connect(self.on_recent_selected)
        tabs.addTab(self.recent_list, "🕐 Recent")

        # Categories tab
        self.categories_list = QListWidget()
        self.categories_list.itemClicked.connect(self.on_category_selected)
        tabs.addTab(self.categories_list, "📂 Categories")

        # Style tabs
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QTabBar::tab {
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)

        return tabs

    def create_hymn_display(self) -> QWidget:
        """Create hymn display area"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Hymn header (number and title)
        self.hymn_header = QLabel("Select a hymn to view")
        self.hymn_header.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background: #ecf0f1;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.hymn_header)

        # Hymn metadata (author, composer, etc.)
        self.hymn_metadata = QLabel()
        self.hymn_metadata.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                padding: 5px 10px;
            }
        """)
        layout.addWidget(self.hymn_metadata)

        # Action buttons
        button_layout = QHBoxLayout()

        self.favorite_btn = QPushButton("⭐ Add to Favorites")
        self.favorite_btn.clicked.connect(self.toggle_favorite)
        self.favorite_btn.setEnabled(False)
        button_layout.addWidget(self.favorite_btn)

        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.clicked.connect(self.copy_hymn)
        self.copy_btn.setEnabled(False)
        button_layout.addWidget(self.copy_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Hymn content (verses)
        self.hymn_content = QTextEdit()
        self.hymn_content.setReadOnly(True)
        font = QFont("Segoe UI", 12)
        self.hymn_content.setFont(font)
        self.hymn_content.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 15px;
                background: white;
            }
        """)
        layout.addWidget(self.hymn_content)

        return widget

    def load_data(self):
        """Load initial data from database"""
        # Update stats
        stats = self.db_manager.get_database_stats()
        self.stats_label.setText(
            f"📊 {stats['total_hymns']} Hymns | {stats['total_categories']} Categories | "
            f"{stats['total_favorites']} Favorites"
        )

        # Load all hymns
        self.load_all_hymns()

        # Load favorites
        self.load_favorites()

        # Load recent
        self.load_recent()

        # Load categories
        self.load_categories()

    def load_all_hymns(self):
        """Load all hymns into list"""
        self.hymns_list.clear()
        hymns = self.db_manager.get_all_hymns()

        for hymn in hymns:
            item = QListWidgetItem(f"#{hymn['number']} - {hymn['title']}")
            item.setData(Qt.ItemDataRole.UserRole, hymn)
            self.hymns_list.addItem(item)

    def load_favorites(self):
        """Load favorite hymns"""
        self.favorites_list.clear()
        favorites = self.db_manager.get_favorites()

        for hymn in favorites:
            item = QListWidgetItem(f"#{hymn['number']} - {hymn['title']}")
            item.setData(Qt.ItemDataRole.UserRole, hymn)
            self.favorites_list.addItem(item)

        if not favorites:
            item = QListWidgetItem("No favorites yet. Click ⭐ to add!")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.favorites_list.addItem(item)

    def load_recent(self):
        """Load recently viewed hymns"""
        self.recent_list.clear()
        recent = self.db_manager.get_recently_viewed(50)

        for hymn in recent:
            item = QListWidgetItem(f"#{hymn['number']} - {hymn['title']}")
            item.setData(Qt.ItemDataRole.UserRole, hymn)
            self.recent_list.addItem(item)

        if not recent:
            item = QListWidgetItem("No recent hymns")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.recent_list.addItem(item)

    def load_categories(self):
        """Load categories"""
        self.categories_list.clear()
        categories = self.db_manager.get_categories()

        for category in categories:
            item = QListWidgetItem(f"{category['name']} ({category['hymn_count']})")
            item.setData(Qt.ItemDataRole.UserRole, category)
            self.categories_list.addItem(item)

    def on_hymn_selected(self, item: QListWidgetItem):
        """Handle hymn selection from all hymns list"""
        hymn_data = item.data(Qt.ItemDataRole.UserRole)
        if hymn_data:
            self.display_hymn(hymn_data)

    def on_favorite_selected(self, item: QListWidgetItem):
        """Handle hymn selection from favorites list"""
        hymn_data = item.data(Qt.ItemDataRole.UserRole)
        if hymn_data:
            self.display_hymn(hymn_data)

    def on_recent_selected(self, item: QListWidgetItem):
        """Handle hymn selection from recent list"""
        hymn_data = item.data(Qt.ItemDataRole.UserRole)
        if hymn_data:
            self.display_hymn(hymn_data)

    def on_category_selected(self, item: QListWidgetItem):
        """Handle category selection"""
        category_data = item.data(Qt.ItemDataRole.UserRole)
        if category_data:
            self.hymns_list.clear()
            hymns = self.db_manager.get_hymns_by_category(category_data["id"])

            for hymn in hymns:
                hymn_item = QListWidgetItem(f"#{hymn['number']} - {hymn['title']}")
                hymn_item.setData(Qt.ItemDataRole.UserRole, hymn)
                self.hymns_list.addItem(hymn_item)

            self.statusBar().showMessage(f"Showing hymns in category: {category_data['name']}")

    def display_hymn(self, hymn_data: dict):
        """Display a hymn"""
        self.current_hymn = hymn_data

        # Update header
        self.hymn_header.setText(f"Hymn #{hymn_data['number']} - {hymn_data['title']}")

        # Update metadata
        metadata_parts = []
        if hymn_data.get("author"):
            metadata_parts.append(f"Author: {hymn_data['author']}")
        if hymn_data.get("composer"):
            metadata_parts.append(f"Composer: {hymn_data['composer']}")
        if hymn_data.get("category_name"):
            metadata_parts.append(f"Category: {hymn_data['category_name']}")
        if hymn_data.get("scripture_reference"):
            metadata_parts.append(f"Scripture: {hymn_data['scripture_reference']}")

        self.hymn_metadata.setText(" | ".join(metadata_parts))

        # Update content
        content = hymn_data["verses"]
        if hymn_data.get("chorus"):
            content += f"\n\nChorus:\n{hymn_data['chorus']}"

        self.hymn_content.setPlainText(content)

        # Update favorite button
        is_fav = self.db_manager.is_favorite(hymn_data["id"])
        self.favorite_btn.setText("❤️ Remove from Favorites" if is_fav else "⭐ Add to Favorites")
        self.favorite_btn.setEnabled(True)
        self.copy_btn.setEnabled(True)

        # Add to recently viewed
        self.db_manager.add_recently_viewed(hymn_data["id"])

        # Update status
        self.statusBar().showMessage(f"Viewing: Hymn #{hymn_data['number']}")

    def toggle_favorite(self):
        """Toggle favorite status of current hymn"""
        if not self.current_hymn:
            return

        hymn_id = self.current_hymn["id"]
        is_fav = self.db_manager.is_favorite(hymn_id)

        if is_fav:
            if self.db_manager.remove_favorite(hymn_id):
                self.favorite_btn.setText("⭐ Add to Favorites")
                self.statusBar().showMessage("Removed from favorites")
        else:
            if self.db_manager.add_favorite(hymn_id):
                self.favorite_btn.setText("❤️ Remove from Favorites")
                self.statusBar().showMessage("Added to favorites")

        # Reload favorites list
        self.load_favorites()

        # Update stats
        stats = self.db_manager.get_database_stats()
        self.stats_label.setText(
            f"📊 {stats['total_hymns']} Hymns | {stats['total_categories']} Categories | "
            f"{stats['total_favorites']} Favorites"
        )

    def copy_hymn(self):
        """Copy current hymn to clipboard"""
        if not self.current_hymn:
            return

        from PySide6.QtWidgets import QApplication

        text = f"Hymn #{self.current_hymn['number']} - {self.current_hymn['title']}\n\n"
        text += self.hymn_content.toPlainText()

        QApplication.clipboard().setText(text)
        self.statusBar().showMessage("Hymn copied to clipboard")

    def on_search(self, text: str):
        """Handle search input"""
        if not text.strip():
            self.load_all_hymns()
            return

        # Search in database
        results = self.db_manager.search_hymns(text)

        self.hymns_list.clear()
        for hymn in results:
            item = QListWidgetItem(f"#{hymn['number']} - {hymn['title']}")
            item.setData(Qt.ItemDataRole.UserRole, hymn)
            self.hymns_list.addItem(item)

        if not results:
            item = QListWidgetItem(f"No results found for '{text}'")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.hymns_list.addItem(item)

        self.statusBar().showMessage(f"Found {len(results)} hymn(s)")