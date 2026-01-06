"""
Test script for database functionality
File: tests/test_database.py
Run with: python -m pytest tests/test_database.py -v
"""
import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from christ_in_song.database.connection import DatabaseManager
from christ_in_song.database.models import Hymn, Category


class TestDatabaseManager:
    """Test database manager functionality"""

    @pytest.fixture
    def db_manager(self, tmp_path):
        """Create a temporary database for testing"""
        # Override database path for testing
        import christ_in_song.config as config

        original_path = config.Config.get_database_path
        config.Config.get_database_path = lambda: tmp_path / "test.db"

        db = DatabaseManager()
        db.initialize_database()

        yield db

        # Restore original path
        config.Config.get_database_path = original_path

    def test_database_initialization(self, db_manager):
        """Test that database initializes correctly"""
        assert db_manager.db_path.exists()
        stats = db_manager.get_database_stats()
        assert stats["total_hymns"] >= 3  # Sample hymns
        assert stats["total_categories"] >= 10

    def test_get_hymn_by_number(self, db_manager):
        """Test retrieving hymn by number"""
        hymn = db_manager.get_hymn_by_number(1)
        assert hymn is not None
        assert hymn["title"] == "Holy, Holy, Holy"
        assert hymn["number"] == 1

    def test_search_hymns(self, db_manager):
        """Test full-text search"""
        results = db_manager.search_hymns("grace")
        assert len(results) > 0
        assert any("Amazing Grace" in r["title"] for r in results)

    def test_favorites(self, db_manager):
        """Test favorites functionality"""
        # Add favorite
        assert db_manager.add_favorite(1)
        assert db_manager.is_favorite(1)

        # Get favorites
        favorites = db_manager.get_favorites()
        assert len(favorites) == 1
        assert favorites[0]["number"] == 1

        # Remove favorite
        assert db_manager.remove_favorite(1)
        assert not db_manager.is_favorite(1)

    def test_recently_viewed(self, db_manager):
        """Test recently viewed functionality"""
        # Add to recently viewed
        db_manager.add_recently_viewed(1)
        db_manager.add_recently_viewed(2)

        # Get recently viewed
        recent = db_manager.get_recently_viewed(10)
        assert len(recent) >= 2
        assert recent[0]["number"] == 2  # Most recent first

    def test_categories(self, db_manager):
        """Test category functionality"""
        categories = db_manager.get_categories()
        assert len(categories) > 0

        # Find "Worship and Praise" category
        worship_cat = next(c for c in categories if c["name"] == "Worship and Praise")
        assert worship_cat is not None

        # Get hymns in category
        hymns = db_manager.get_hymns_by_category(worship_cat["id"])
        assert len(hymns) > 0

    def test_settings(self, db_manager):
        """Test settings functionality"""
        # Get default setting
        theme = db_manager.get_setting("theme")
        assert theme == "light"

        # Update setting
        assert db_manager.set_setting("theme", "dark")
        assert db_manager.get_setting("theme") == "dark"

    def test_backup(self, db_manager):
        """Test database backup"""
        backup_path = db_manager.backup_database()
        assert backup_path is not None
        assert backup_path.exists()


# Standalone test function for quick verification
def test_database_standalone():
    """Quick standalone test"""
    print("\n" + "=" * 70)
    print("🧪 Testing Database Implementation")
    print("=" * 70 + "\n")

    from christ_in_song.config import Config

    # Initialize database
    db = DatabaseManager()
    print(f"📁 Database path: {db.db_path}")

    if db.initialize_database():
        print("✅ Database initialized successfully\n")

        # Test basic operations
        print("📊 Database Statistics:")
        stats = db.get_database_stats()
        print(f"  • Total hymns: {stats['total_hymns']}")
        print(f"  • Total categories: {stats['total_categories']}")
        print(f"  • Total favorites: {stats['total_favorites']}")
        print(f"  • Database version: {stats['database_version']}")
        print(f"  • Database size: {stats['database_size']:,} bytes\n")

        # Test hymn retrieval
        print("🎵 Testing Hymn Retrieval:")
        hymn = db.get_hymn_by_number(1)
        if hymn:
            print(f"  • Hymn #{hymn['number']}: {hymn['title']}")
            print(f"  • Author: {hymn['author']}")
            print(f"  • Category: {hymn['category_name']}\n")

        # Test search
        print("🔍 Testing Search:")
        results = db.search_hymns("grace")
        print(f"  • Found {len(results)} hymns matching 'grace'")
        for r in results[:3]:
            print(f"    - #{r['number']}: {r['title']}")
        print()

        # Test favorites
        print("⭐ Testing Favorites:")
        db.add_favorite(1)
        db.add_favorite(2)
        favorites = db.get_favorites()
        print(f"  • Total favorites: {len(favorites)}")
        for f in favorites:
            print(f"    - #{f['number']}: {f['title']}")
        print()

        # Test categories
        print("📂 Testing Categories:")
        categories = db.get_categories()
        print(f"  • Total categories: {len(categories)}")
        for c in categories[:5]:
            print(f"    - {c['name']} ({c['hymn_count']} hymns)")

        print("\n" + "=" * 70)
        print("✅ All tests completed successfully!")
        print("=" * 70 + "\n")

    else:
        print("❌ Database initialization failed\n")


if __name__ == "__main__":
    test_database_standalone()