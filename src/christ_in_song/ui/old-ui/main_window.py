"""
Main application window with complete UI implementation
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QLineEdit, QScrollArea, QFrame,
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QIcon, QPalette, QColor
from christ_in_song.config import Config
import re
import html


class ModernButton(QPushButton):
    """Custom styled button with hover effects"""
    
    def __init__(self, text, icon="", color="#3498db", parent=None):
        super().__init__(text, parent)
        self.default_color = color
        self.hover_color = self._darken_color(color)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_style()
    
    def _darken_color(self, color):
        """Darken a color by 15% for hover effect"""
        color_map = {
            "#3498db": "#2980b9",
            "#e74c3c": "#c0392b",
            "#f39c12": "#e67e22",
            "#95a5a6": "#7f8c8d",
            "#27ae60": "#229954",
            "#ffffff": "#ecf0f1"
        }
        return color_map.get(color, color)
    
    def _update_style(self):
        """Update button stylesheet"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.default_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(self.hover_color)};
            }}
        """)


class NavButton(QPushButton):
    """Navigation sidebar button"""
    
    def __init__(self, text, icon="", parent=None):
        super().__init__(f"{icon} {text}", parent)
        self.is_active = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_style()
    
    def set_active(self, active):
        """Set button active state"""
        self.is_active = active
        self._update_style()
    
    def _update_style(self):
        """Update button stylesheet"""
        if self.is_active:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: 600;
                    text-align: left;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #2c3e50;
                    border: none;
                    border-radius: 6px;
                    padding: 12px 20px;
                    font-size: 14px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e8f4f8;
                }
            """)


class MainWindow(QMainWindow):
    """Main application window with complete UI"""
    
    # Signals
    hymn_changed = Signal(int)
    
    def __init__(self, db_manager=None):
        """Initialize the main window"""
        super().__init__()
        self.db_manager = db_manager
        self.current_hymn = 1
        self.total_hymns = 695
        self.font_size = 14
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the complete user interface"""
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.VERSION}")
        self.setGeometry(100, 50, 1300, 900)
        
        # Set window icon if available
        # icon_path = Config.get_resource_path("icons/app_icon.ico")
        # if icon_path.exists():
        #     self.setWindowIcon(QIcon(str(icon_path)))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar and main content
        sidebar = self.create_sidebar()
        main_content = self.create_main_content()
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(main_content)
        
        # Create status bar
        self.create_status_bar()
        
        # Apply global styles
        self.apply_styles()
    
    def create_sidebar(self):
        """Create the navigation sidebar"""
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-right: 1px solid #bdc3c7;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Header
        header = QLabel("Navigation")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px 0;
        """)
        layout.addWidget(header)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search hymns...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 20px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.search_box.returnPressed.connect(self.on_search)
        layout.addWidget(self.search_box)
        
        layout.addSpacing(10)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("home", "🏠 Home", True),
            ("browse", "📚 Browse All Hymns", False),
            ("favorites", "⭐ Favorites", False),
            ("recent", "🕐 Recently Viewed", False),
            ("categories", "🗂️ Categories", False),
            ("dialpad", "🎹 Number Dialpad", False),
        ]
        
        for key, text, is_active in nav_items:
            btn = NavButton(text)
            btn.set_active(is_active)
            btn.clicked.connect(lambda checked, k=key: self.on_nav_click(k))
            self.nav_buttons[key] = btn
            layout.addWidget(btn)
        
        # Spacer
        layout.addStretch()
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(separator)
        
        # Settings button
        settings_btn = NavButton("⚙️ Settings")
        settings_btn.clicked.connect(self.on_settings_click)
        layout.addWidget(settings_btn)
        
        return sidebar
    
    def create_main_content(self):
        """Create the main content area"""
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Hymn header
        header = self.create_hymn_header()
        layout.addWidget(header)
        
        # Hymn content area
        content = self.create_hymn_content()
        layout.addWidget(content, 1)
        
        # Navigation controls
        controls = self.create_nav_controls()
        layout.addWidget(controls)
        
        return main_widget
    
    def create_hymn_header(self):
        """Create hymn display header"""
        header_widget = QFrame()
        header_widget.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-bottom: 1px solid #bdc3c7;
            }
        """)
        header_widget.setFixedHeight(80)
        
        layout = QHBoxLayout(header_widget)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Hymn number badge
        self.hymn_badge = QLabel("1")
        self.hymn_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hymn_badge.setFixedSize(50, 50)
        self.hymn_badge.setStyleSheet("""
            QLabel {
                background-color: #3498db;
                color: white;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.hymn_badge)
        
        # Title and metadata
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        self.hymn_title = QLabel("Holy, Holy, Holy")
        self.hymn_title.setStyleSheet("""
            font-family: Georgia, serif;
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
        """)
        title_layout.addWidget(self.hymn_title)
        
        self.hymn_metadata = QLabel("Reginald Heber, 1826 • John B. Dykes, 1861")
        self.hymn_metadata.setStyleSheet("""
            font-size: 12px;
            color: #7f8c8d;
        """)
        title_layout.addWidget(self.hymn_metadata)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Action buttons
        self.fav_btn = ModernButton("⭐", color="#f39c12")
        self.fav_btn.setFixedSize(50, 40)
        self.fav_btn.setToolTip("Add to Favorites")
        self.fav_btn.clicked.connect(self.toggle_favorite)
        layout.addWidget(self.fav_btn)
        
        self.print_btn = ModernButton("🖨️", color="#95a5a6")
        self.print_btn.setFixedSize(50, 40)
        self.print_btn.setToolTip("Print Hymn")
        self.print_btn.clicked.connect(self.print_hymn)
        layout.addWidget(self.print_btn)
        
        return header_widget
    
    def create_hymn_content(self):
        """Create hymn content display area"""
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)
        
        # Content widget
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Text display
        self.hymn_content = QTextEdit()
        self.hymn_content.setReadOnly(True)
        self.hymn_content.setFrameShape(QFrame.Shape.NoFrame)
        
        font = QFont("Georgia", self.font_size)
        self.hymn_content.setFont(font)
        
        self.hymn_content.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 20px;
                line-height: 1.6;
            }
        """)
        
        # Load sample hymn
        self.display_sample_hymn()
        
        layout.addWidget(self.hymn_content)
        scroll.setWidget(content_widget)
        
        return scroll
    
    def create_nav_controls(self):
        """Create navigation controls"""
        control_widget = QFrame()
        control_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #dee2e6;
            }
        """)
        control_widget.setFixedHeight(70)
        
        layout = QHBoxLayout(control_widget)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(10)
        
        # Previous button
        prev_btn = ModernButton("← Previous")
        prev_btn.setFixedWidth(120)
        prev_btn.clicked.connect(self.previous_hymn)
        layout.addWidget(prev_btn)
        
        # Hymn counter
        self.hymn_counter = QLabel(f"Hymn {self.current_hymn} of {self.total_hymns}")
        self.hymn_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hymn_counter.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                border-radius: 6px;
                padding: 12px 30px;
                font-size: 14px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(self.hymn_counter, 1)
        
        # Next button
        next_btn = ModernButton("Next →")
        next_btn.setFixedWidth(120)
        next_btn.clicked.connect(self.next_hymn)
        layout.addWidget(next_btn)
        
        # Font size controls
        font_down = ModernButton("A-", color="#95a5a6")
        font_down.setFixedSize(50, 45)
        font_down.setToolTip("Decrease Font Size")
        font_down.clicked.connect(self.decrease_font)
        layout.addWidget(font_down)
        
        font_up = ModernButton("A+", color="#95a5a6")
        font_up.setFixedSize(50, 45)
        font_up.setToolTip("Increase Font Size")
        font_up.clicked.connect(self.increase_font)
        layout.addWidget(font_up)
        
        # Presentation mode
        present_btn = ModernButton("🖥️ Present", color="#e74c3c")
        present_btn.setFixedWidth(140)
        present_btn.clicked.connect(self.enter_presentation_mode)
        layout.addWidget(present_btn)
        
        return control_widget
    
    def create_status_bar(self):
        """Create status bar"""
        status = self.statusBar()
        status.setStyleSheet("""
            QStatusBar {
                background-color: #34495e;
                color: #ecf0f1;
                font-size: 12px;
                padding: 5px;
            }
        """)
        
        db_status = "Database connected" if self.db_manager else "Database stub mode"
        status.showMessage(f"Ready • {db_status} • {self.total_hymns} hymns available")
        
        # Version label
        version_label = QLabel(f"v{Config.VERSION}")
        version_label.setStyleSheet("color: #95a5a6;")
        status.addPermanentWidget(version_label)
    
    def apply_styles(self):
        """Apply global application styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
        """)
    
    # Event handlers
    def on_nav_click(self, key):
        """Handle navigation button click"""
        # Update active state
        for k, btn in self.nav_buttons.items():
            btn.set_active(k == key)
        
        # Handle navigation
        if key == "home":
            self.statusBar().showMessage("Home view")
        elif key == "browse":
            self.statusBar().showMessage("Browse all hymns")
        elif key == "favorites":
            self.statusBar().showMessage("Favorites view")
        elif key == "recent":
            self.statusBar().showMessage("Recently viewed hymns")
        elif key == "categories":
            self.statusBar().showMessage("Categories view")
        elif key == "dialpad":
            self.show_dialpad()
    
    def on_search(self):
        """Handle search"""
        query = self.search_box.text()
        if query:
            self.statusBar().showMessage(f"Searching for: {query}")
    
    def on_settings_click(self):
        """Open settings"""
        self.statusBar().showMessage("Settings panel")
    
    def previous_hymn(self):
        """Go to previous hymn"""
        if self.current_hymn > 1:
            self.current_hymn -= 1
            self.update_hymn_display()
    
    def next_hymn(self):
        """Go to next hymn"""
        if self.current_hymn < self.total_hymns:
            self.current_hymn += 1
            self.update_hymn_display()
    
    def update_hymn_display(self):
        """Update hymn display"""
        self.hymn_badge.setText(str(self.current_hymn))
        self.hymn_counter.setText(f"Hymn {self.current_hymn} of {self.total_hymns}")
        self.statusBar().showMessage(f"Displaying Hymn #{self.current_hymn}")
        self.hymn_changed.emit(self.current_hymn)
    
    def increase_font(self):
        """Increase font size"""
        if self.font_size < 24:
            self.font_size += 2
            self.hymn_content.setFont(QFont("Georgia", self.font_size))
            self.statusBar().showMessage(f"Font size: {self.font_size}pt")
    
    def decrease_font(self):
        """Decrease font size"""
        if self.font_size > 10:
            self.font_size -= 2
            self.hymn_content.setFont(QFont("Georgia", self.font_size))
            self.statusBar().showMessage(f"Font size: {self.font_size}pt")
    
    def toggle_favorite(self):
        """Toggle favorite status"""
        self.statusBar().showMessage(f"Hymn #{self.current_hymn} added to favorites")
    
    def print_hymn(self):
        """Print current hymn"""
        self.statusBar().showMessage(f"Printing Hymn #{self.current_hymn}")
    
    def enter_presentation_mode(self):
        """Enter presentation mode"""
        self.statusBar().showMessage("Entering presentation mode...")
        # TODO: Implement presentation mode window
    
    def show_dialpad(self):
        """Show number dialpad"""
        self.statusBar().showMessage("Opening number dialpad...")
        # TODO: Implement dialpad dialog
    
    def display_sample_hymn(self):
        """Display a sample hymn"""
        sample_text = """<div style="font-family: Georgia; line-height: 1.8;">
<p style="font-weight: bold; font-size: 16px; color: #2c3e50;">Verse 1:</p>
<p style="color: #34495e;">
Holy, holy, holy! Lord God Almighty!<br>
Early in the morning our song shall rise to Thee;<br>
Holy, holy, holy! Merciful and mighty!<br>
God in three Persons, blessed Trinity!
</p>

<p style="font-weight: bold; font-size: 16px; color: #2c3e50; margin-top: 20px;">Verse 2:</p>
<p style="color: #34495e;">
Holy, holy, holy! All the saints adore Thee,<br>
Casting down their golden crowns around the glassy sea;<br>
Cherubim and seraphim falling down before Thee,<br>
Which wert, and art, and evermore shalt be.
</p>

<p style="font-weight: bold; font-size: 16px; color: #2c3e50; margin-top: 20px;">Verse 3:</p>
<p style="color: #34495e;">
Holy, holy, holy! Though the darkness hide Thee,<br>
Though the eye of sinful man Thy glory may not see,<br>
Only Thou art holy; there is none beside Thee<br>
Perfect in power, in love, and purity.
</p>

<p style="font-weight: bold; font-size: 16px; color: #2c3e50; margin-top: 20px;">Verse 4:</p>
<p style="color: #34495e;">
Holy, holy, holy! Lord God Almighty!<br>
All Thy works shall praise Thy name in earth and sky and sea;<br>
Holy, holy, holy! Merciful and mighty!<br>
God in three Persons, blessed Trinity!
</p>
</div>"""
        self.hymn_content.setHtml(sample_text)
    
    def display_hymn(self, hymn_data: dict):
        """Display hymn data"""
        self.current_hymn = hymn_data.get('number', 1)
        self.hymn_badge.setText(str(self.current_hymn))
        self.hymn_title.setText(hymn_data.get('title', 'Unknown'))
        
        author = hymn_data.get('author', '')
        composer = hymn_data.get('composer', '')
        year = hymn_data.get('year', '')
        
        metadata_parts = []
        if author:
            metadata_parts.append(author)
        if composer:
            metadata_parts.append(composer)
        if year:
            metadata_parts[-1] += f", {year}"
        
        self.hymn_metadata.setText(" • ".join(metadata_parts))
        
        # Format verses
        verses = hymn_data.get('verses', [])
        html_content = '<div style="font-family: Georgia; line-height: 1.8;">'
        
        for i, verse in enumerate(verses, 1):
            html_content += f'''
<p style="font-weight: bold; font-size: 16px; color: #2c3e50; margin-top: 20px;">Verse {i}:</p>
<p style="color: #34495e;">{verse.replace(chr(10), '<br>')}</p>
'''
        
        html_content += '</div>'
        self.hymn_content.setHtml(html_content)
        
        self.update_hymn_display()