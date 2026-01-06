"""
Database connection manager for Christ In Song Hymnal
File: src/christ_in_song/database/connection.py

INSTRUCTIONS: Replace your entire connection.py file with this content
"""
import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from christ_in_song.config import Config
from christ_in_song.database.schema import (
    SCHEMA,
    DEFAULT_CATEGORIES,
    SAMPLE_HYMNS,
    DEFAULT_SETTINGS,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations"""

    def __init__(self):
        self.db_path = Config.get_database_path()
        self._connection: Optional[sqlite3.Connection] = None
        logger.info(f"Database manager initialized with path: {self.db_path}")

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def initialize_database(self) -> bool:
        """Initialize the database with schema and default data"""
        try:
            logger.info("Initializing database...")

            # Check if database already exists
            is_new_db = not self.db_path.exists()

            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Execute schema
                logger.info("Creating database schema...")
                cursor.executescript(SCHEMA)

                if is_new_db:
                    logger.info("New database detected. Loading default data...")

                    # Insert default categories
                    cursor.executemany(
                        "INSERT INTO categories (name, description) VALUES (?, ?)",
                        DEFAULT_CATEGORIES,
                    )
                    logger.info(f"Inserted {len(DEFAULT_CATEGORIES)} categories")

                    # Insert sample hymns
                    for hymn in SAMPLE_HYMNS:
                        # Get category_id
                        cursor.execute(
                            "SELECT id FROM categories WHERE name = ?",
                            (hymn["category"],),
                        )
                        category_row = cursor.fetchone()
                        category_id = category_row["id"] if category_row else None

                        cursor.execute(
                            """
                            INSERT INTO hymns 
                            (number, title, verses, chorus, category_id, author, composer, year, scripture_reference)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                hymn["number"],
                                hymn["title"],
                                hymn["verses"],
                                hymn.get("chorus"),
                                category_id,
                                hymn.get("author"),
                                hymn.get("composer"),
                                hymn.get("year"),
                                hymn.get("scripture_reference"),
                            ),
                        )
                    logger.info(f"Inserted {len(SAMPLE_HYMNS)} sample hymns")

                    # Insert default settings
                    cursor.executemany(
                        "INSERT INTO settings (key, value, description) VALUES (?, ?, ?)",
                        DEFAULT_SETTINGS,
                    )
                    logger.info(f"Inserted {len(DEFAULT_SETTINGS)} default settings")

                # Verify database
                cursor.execute("SELECT COUNT(*) as count FROM hymns")
                hymn_count = cursor.fetchone()["count"]
                logger.info(f"Database contains {hymn_count} hymns")

                cursor.execute("SELECT COUNT(*) as count FROM categories")
                category_count = cursor.fetchone()["count"]
                logger.info(f"Database contains {category_count} categories")

            logger.info("✅ Database initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}", exc_info=True)
            return False

    def backup_database(self) -> Optional[Path]:
        """Create a backup of the database"""
        try:
            from datetime import datetime
            import shutil

            backup_dir = Config.get_backup_dir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"christ_in_song_backup_{timestamp}.db"

            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to: {backup_path}")
            return backup_path

        except Exception as e:
            logger.error(f"Failed to backup database: {e}")
            return None

    def get_hymn_by_number(self, number: int) -> Optional[Dict[str, Any]]:
        """Get a hymn by its number"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT h.*, c.name as category_name
                    FROM hymns h
                    LEFT JOIN categories c ON h.category_id = c.id
                    WHERE h.number = ?
                    """,
                    (number,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error fetching hymn {number}: {e}")
            return None

    def search_hymns(self, query: str) -> List[Dict[str, Any]]:
        """Search hymns using full-text search"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT h.*, c.name as category_name
                    FROM hymns h
                    LEFT JOIN categories c ON h.category_id = c.id
                    WHERE h.id IN (
                        SELECT rowid FROM hymns_fts 
                        WHERE hymns_fts MATCH ?
                    )
                    ORDER BY h.number
                    """,
                    (query,),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error searching hymns: {e}")
            return []

    def get_all_hymns(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all hymns"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT h.*, c.name as category_name
                    FROM hymns h
                    LEFT JOIN categories c ON h.category_id = c.id
                    ORDER BY h.number
                """
                if limit:
                    query += f" LIMIT {limit}"
                cursor.execute(query)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching all hymns: {e}")
            return []

    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorite hymns"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT h.*, c.name as category_name, f.added_at
                    FROM favorites f
                    JOIN hymns h ON f.hymn_id = h.id
                    LEFT JOIN categories c ON h.category_id = c.id
                    ORDER BY f.added_at DESC
                    """
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching favorites: {e}")
            return []

    def add_favorite(self, hymn_id: int) -> bool:
        """Add a hymn to favorites"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO favorites (hymn_id) VALUES (?)",
                    (hymn_id,),
                )
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error adding favorite: {e}")
            return False

    def remove_favorite(self, hymn_id: int) -> bool:
        """Remove a hymn from favorites"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM favorites WHERE hymn_id = ?", (hymn_id,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error removing favorite: {e}")
            return False

    def is_favorite(self, hymn_id: int) -> bool:
        """Check if a hymn is in favorites"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT COUNT(*) as count FROM favorites WHERE hymn_id = ?",
                    (hymn_id,),
                )
                return cursor.fetchone()["count"] > 0
        except Exception as e:
            logger.error(f"Error checking favorite status: {e}")
            return False

    def add_recently_viewed(self, hymn_id: int) -> bool:
        """Add a hymn to recently viewed"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO recently_viewed (hymn_id) VALUES (?)",
                    (hymn_id,),
                )

                # Update usage stats
                cursor.execute(
                    """
                    INSERT INTO usage_stats (hymn_id, view_count, last_viewed)
                    VALUES (?, 1, CURRENT_TIMESTAMP)
                    ON CONFLICT(hymn_id) DO UPDATE SET
                        view_count = view_count + 1,
                        last_viewed = CURRENT_TIMESTAMP
                    """,
                    (hymn_id,),
                )
                return True
        except Exception as e:
            logger.error(f"Error adding to recently viewed: {e}")
            return False

    def get_recently_viewed(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recently viewed hymns"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT DISTINCT h.*, c.name as category_name, r.viewed_at
                    FROM recently_viewed r
                    JOIN hymns h ON r.hymn_id = h.id
                    LEFT JOIN categories c ON h.category_id = c.id
                    ORDER BY r.viewed_at DESC
                    LIMIT ?
                    """,
                    (limit,),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching recently viewed: {e}")
            return []

    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT c.*, COUNT(h.id) as hymn_count
                    FROM categories c
                    LEFT JOIN hymns h ON c.id = h.category_id
                    GROUP BY c.id
                    ORDER BY c.name
                    """
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            return []

    def get_hymns_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """Get all hymns in a category"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT h.*, c.name as category_name
                    FROM hymns h
                    LEFT JOIN categories c ON h.category_id = c.id
                    WHERE h.category_id = ?
                    ORDER BY h.number
                    """,
                    (category_id,),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching hymns by category: {e}")
            return []

    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
                row = cursor.fetchone()
                return row["value"] if row else None
        except Exception as e:
            logger.error(f"Error fetching setting {key}: {e}")
            return None

    def set_setting(self, key: str, value: str) -> bool:
        """Set a setting value"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO settings (key, value) VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET 
                        value = excluded.value,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (key, value),
                )
                return True
        except Exception as e:
            logger.error(f"Error setting {key}: {e}")
            return False

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                stats = {}

                # Count hymns
                cursor.execute("SELECT COUNT(*) as count FROM hymns")
                stats["total_hymns"] = cursor.fetchone()["count"]

                # Count categories
                cursor.execute("SELECT COUNT(*) as count FROM categories")
                stats["total_categories"] = cursor.fetchone()["count"]

                # Count favorites
                cursor.execute("SELECT COUNT(*) as count FROM favorites")
                stats["total_favorites"] = cursor.fetchone()["count"]

                # Database size
                stats["database_size"] = self.db_path.stat().st_size

                # Version
                cursor.execute("SELECT value FROM db_metadata WHERE key = 'version'")
                stats["database_version"] = cursor.fetchone()["value"]

                return stats

        except Exception as e:
            logger.error(f"Error fetching database stats: {e}")
            return {}