"""
Main application window with plain text rendering and database support
"""
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, 
                                QPushButton, QHBoxLayout, QPlainTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from christ_in_song.config import Config
import re
import html


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, db_manager=None):
        """
        Initialize the main window
        
        Args:
            db_manager: DatabaseManager instance (optional)
        """
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.VERSION}")
        self.setGeometry(100, 100, Config.DEFAULT_WINDOW_WIDTH, Config.DEFAULT_WINDOW_HEIGHT)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add header
        header_label = QLabel("🎵 Christ In Song Hymnal")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                color: #2c3e50;
                background: #ecf0f1;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        layout.addWidget(header_label)
        
        # Create hymn display area using QPlainTextEdit for pure text
        self.hymn_content = QPlainTextEdit()
        self.hymn_content.setReadOnly(True)
        
        # Set font for hymn content
        font = QFont("Segoe UI", 12)
        self.hymn_content.setFont(font)
        
        # Style the text edit
        self.hymn_content.setStyleSheet("""
            QPlainTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 15px;
                background: white;
                line-height: 1.6;
            }
        """)
        
        # Add sample hymn text
        self.display_sample_hymn()
        
        layout.addWidget(self.hymn_content)
        
        # Add control buttons
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("Load Test Hymn")
        test_btn.clicked.connect(self.display_sample_hymn)
        test_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        button_layout.addWidget(test_btn)
        
        test_html_btn = QPushButton("Test HTML Input")
        test_html_btn.clicked.connect(self.display_html_test)
        test_html_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        button_layout.addWidget(test_html_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.hymn_content.clear)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        # Add status bar
        db_status = "Database connected" if self.db_manager else "Database stub mode"
        self.statusBar().showMessage(f"Ready - {db_status} - Plain text mode active")
    
    def display_sample_hymn(self):
        """Display a sample hymn in plain text format"""
        sample_text = """Hymn #1: Holy, Holy, Holy

Verse 1:
Holy, holy, holy! Lord God Almighty!
Early in the morning our song shall rise to Thee;
Holy, holy, holy! Merciful and mighty!
God in three Persons, blessed Trinity!

Verse 2:
Holy, holy, holy! All the saints adore Thee,
Casting down their golden crowns around the glassy sea;
Cherubim and seraphim falling down before Thee,
Which wert, and art, and evermore shalt be.

Verse 3:
Holy, holy, holy! Though the darkness hide Thee,
Though the eye of sinful man Thy glory may not see,
Only Thou art holy; there is none beside Thee
Perfect in power, in love, and purity.

Verse 4:
Holy, holy, holy! Lord God Almighty!
All Thy works shall praise Thy name in earth and sky and sea;
Holy, holy, holy! Merciful and mighty!
God in three Persons, blessed Trinity!

Author: Reginald Heber, 1826
Composer: John B. Dykes, 1861
"""
        self.hymn_content.setPlainText(sample_text)
        self.statusBar().showMessage("Sample hymn loaded")
    
    def display_html_test(self):
        """Test displaying HTML content as plain text"""
        html_content = """<h1>Hymn #123</h1>
<p><strong>Title:</strong> Amazing Grace</p>
<div class="verse">
<p>Amazing grace! How sweet the sound<br/>
That saved a wretch like me!<br/>
I once was lost, but now am found;<br/>
Was blind, but now I see.</p>
</div>
<p><em>Author:</em> John Newton &amp; more &lt;tags&gt;</p>"""
        
        # Clean and display
        cleaned = self.clean_html_to_text(html_content)
        self.hymn_content.setPlainText(f"--- HTML INPUT CLEANED ---\n\n{cleaned}")
        self.statusBar().showMessage("HTML tags stripped successfully")
    
    def display_hymn(self, hymn_data: dict):
        """
        Display hymn data in a safe, readable format
        
        Args:
            hymn_data: Dictionary containing hymn information
                - number: Hymn number
                - title: Hymn title
                - verses: List of verse texts or HTML content
                - author: Author name (optional)
                - composer: Composer name (optional)
                - chorus: Chorus text (optional)
                - year: Year (optional)
        """
        lines = []
        
        # Add title and number
        title = self.clean_html_to_text(hymn_data.get('title', 'Unknown'))
        lines.append(f"Hymn #{hymn_data.get('number', 'N/A')}: {title}")
        lines.append("")
        
        # Add verses
        verses = hymn_data.get('verses', [])
        for i, verse in enumerate(verses, 1):
            lines.append(f"Verse {i}:")
            # Clean the verse text (remove HTML tags if any)
            clean_verse = self.clean_html_to_text(verse)
            lines.append(clean_verse)
            lines.append("")
        
        # Add chorus if present
        if hymn_data.get('chorus'):
            lines.append("Chorus:")
            clean_chorus = self.clean_html_to_text(hymn_data['chorus'])
            lines.append(clean_chorus)
            lines.append("")
        
        # Add author and composer
        if hymn_data.get('author'):
            author = self.clean_html_to_text(hymn_data['author'])
            lines.append(f"Author: {author}")
        if hymn_data.get('composer'):
            composer = self.clean_html_to_text(hymn_data['composer'])
            lines.append(f"Composer: {composer}")
        if hymn_data.get('year'):
            lines.append(f"Year: {hymn_data['year']}")
        
        # Join all lines and display as plain text
        hymn_text = "\n".join(lines)
        self.hymn_content.setPlainText(hymn_text)
        self.statusBar().showMessage(f"Displaying Hymn #{hymn_data.get('number', 'N/A')}")
    
    @staticmethod
    def clean_html_to_text(text: str) -> str:
        """
        Convert HTML content to plain text
        
        This method:
        1. Converts common HTML tags to readable text
        2. Removes all HTML tags
        3. Decodes HTML entities
        4. Cleans up whitespace
        
        Args:
            text: Text that may contain HTML tags
            
        Returns:
            Clean plain text without HTML
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Convert <br>, <br/>, <br /> to newlines
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        
        # Convert <p> tags to paragraphs with double newlines
        text = re.sub(r'</p>\s*<p>', '\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</?p>', '\n', text, flags=re.IGNORECASE)
        
        # Convert <div> tags to newlines
        text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
        
        # Convert heading tags to text with newlines
        text = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\n\1\n', text, flags=re.IGNORECASE)
        
        # Remove all other HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Clean up excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Max 2 consecutive newlines
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single space
        text = re.sub(r' *\n *', '\n', text)  # Remove spaces around newlines
        
        return text.strip()
    
    def set_font_size(self, size: int):
        """
        Change the font size of hymn content
        
        Args:
            size: Font size in points (recommended: 10-20)
        """
        font = self.hymn_content.font()
        font.setPointSize(size)
        self.hymn_content.setFont(font)
        self.statusBar().showMessage(f"Font size changed to {size}pt")
    
    def display_raw_content(self, content: str):
        """
        Display raw content from database, automatically cleaning HTML
        
        Args:
            content: Raw content string (may contain HTML)
        """
        cleaned = self.clean_html_to_text(content)
        self.hymn_content.setPlainText(cleaned)
        self.statusBar().showMessage("Raw content displayed")
    
    def load_hymn_from_database(self, hymn_number: int):
        """
        Load a hymn from the database and display it
        
        Args:
            hymn_number: The hymn number to load
        """
        if not self.db_manager:
            self.statusBar().showMessage("Database not connected")
            return
        
        # TODO: Implement database query when database is ready
        # For now, show a placeholder message
        self.hymn_content.setPlainText(
            f"Loading Hymn #{hymn_number} from database...\n\n"
            "Database integration coming soon!"
        )
        self.statusBar().showMessage(f"Requested Hymn #{hymn_number}")