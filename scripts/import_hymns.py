"""
Import hymns from the cis-hymnals JSON file
File: scripts/import_hymns.py

Usage: python scripts/import_hymns.py
"""
import json
import sys
import logging
from pathlib import Path
from urllib.request import urlopen

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from christ_in_song.config import Config
from christ_in_song.database.connection import DatabaseManager

# URL to the English hymnal JSON
HYMNAL_URL = "https://raw.githubusercontent.com/TinasheMzondiwa/cis-hymnals/main/english.json"

# Category mapping from content to our categories
CATEGORY_MAPPING = {
    "worship": "Worship and Praise",
    "praise": "Worship and Praise",
    "adore": "Worship and Praise",
    "glory": "Worship and Praise",
    "prayer": "Prayer",
    "pray": "Prayer",
    "faith": "Faith and Trust",
    "trust": "Faith and Trust",
    "believe": "Faith and Trust",
    "love": "Love of God",
    "salvation": "Salvation",
    "saved": "Salvation",
    "grace": "Salvation",
    "redeemed": "Salvation",
    "coming": "Second Coming",
    "return": "Second Coming",
    "service": "Service",
    "serve": "Service",
    "comfort": "Comfort and Peace",
    "peace": "Comfort and Peace",
    "rest": "Comfort and Peace",
    "heaven": "Heaven",
    "home": "Heaven",
    "eternal": "Heaven",
    "christmas": "Christmas",
    "bethlehem": "Christmas",
    "easter": "Easter",
    "cross": "Salvation",
    "calvary": "Salvation",
    "testimony": "Testimony",
    "witness": "Testimony",
}


def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def download_hymnal_json(url: str):
    """Download the hymnal JSON from GitHub"""
    logger = logging.getLogger(__name__)
    logger.info(f"Downloading hymnal data from: {url}")

    try:
        with urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            logger.info(f"Successfully downloaded hymnal data")
            return data
    except Exception as e:
        logger.error(f"Failed to download hymnal: {e}")
        raise


def determine_category(hymn_data: dict, db_manager: DatabaseManager) -> int:
    """Determine the best category for a hymn based on its content"""
    # Get all categories
    categories = db_manager.get_categories()
    category_map = {cat["name"]: cat["id"] for cat in categories}

    # Default to "Christian Life"
    default_category = category_map.get("Christian Life")

    # Check title and content for keywords
    title = hymn_data.get("title", "").lower()
    content = hymn_data.get("content", "").lower()
    combined_text = f"{title} {content[:500]}"  # First 500 chars of content

    # Try to match keywords - prioritize by order
    for keyword, category_name in CATEGORY_MAPPING.items():
        if keyword in combined_text:
            cat_id = category_map.get(category_name)
            if cat_id:
                return cat_id

    return default_category


def parse_hymn_content(content: str) -> tuple:
    """Parse hymn content into verses and chorus"""
    if not content:
        return "", None

    # The content is already formatted with verse numbers
    # Just clean it up a bit
    lines = content.strip().split("\n")
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            cleaned_lines.append(line)
    
    # Join with proper spacing
    verses_text = "\n".join(cleaned_lines)
    
    # For now, we don't extract chorus separately
    # The format doesn't clearly separate it
    return verses_text, None


def import_hymns(db_manager: DatabaseManager, hymns_data: list):
    """Import hymns from the JSON data into the database"""
    logger = logging.getLogger(__name__)

    if not hymns_data or not isinstance(hymns_data, list):
        logger.error("Invalid hymnal data format - expected a list of hymns")
        return

    logger.info(f"Found {len(hymns_data)} hymns to import")

    # Clear existing hymns (optional - comment out if you want to keep sample data)
    logger.info("Clearing existing hymns...")
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hymns")
        cursor.execute("DELETE FROM hymns_fts")
        logger.info("Existing hymns cleared")

    imported_count = 0
    error_count = 0

    for hymn_data in hymns_data:
        try:
            # Extract hymn data
            number = hymn_data.get("number")
            title = hymn_data.get("title", "").strip()
            content = hymn_data.get("content", "").strip()

            if not number or not title or not content:
                logger.warning(f"Skipping hymn with incomplete data: {hymn_data.get('number', '?')}")
                error_count += 1
                continue

            # Parse content into verses
            verses, chorus = parse_hymn_content(content)

            # Determine category
            category_id = determine_category(hymn_data, db_manager)

            # Insert hymn
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO hymns 
                    (number, title, verses, chorus, category_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (number, title, verses, chorus, category_id),
                )

            imported_count += 1

            # Progress indicator
            if imported_count % 50 == 0:
                logger.info(f"Imported {imported_count} hymns...")

        except Exception as e:
            logger.error(f"Error importing hymn {hymn_data.get('number', '?')}: {e}")
            error_count += 1
            continue

    logger.info("=" * 70)
    logger.info(f"✅ Import completed!")
    logger.info(f"  Successfully imported: {imported_count} hymns")
    logger.info(f"  Errors: {error_count}")
    logger.info("=" * 70)


def main():
    """Main import function"""
    setup_logging()
    logger = logging.getLogger(__name__)

    print("\n" + "=" * 70)
    print("🎵 CHRIST IN SONG - HYMNAL IMPORT SCRIPT")
    print("=" * 70 + "\n")

    try:
        # Initialize database
        logger.info("Initializing database connection...")
        db_manager = DatabaseManager()

        # Make sure database is initialized
        if not db_manager.db_path.exists():
            logger.info("Database doesn't exist, initializing...")
            db_manager.initialize_database()
        else:
            # Ensure database schema is up to date
            db_manager.initialize_database()

        # Download hymnal JSON
        logger.info("Downloading hymnal data from GitHub...")
        hymnal_data = download_hymnal_json(HYMNAL_URL)

        # Check data structure
        if isinstance(hymnal_data, list):
            # It's a direct list of hymns
            hymns = hymnal_data
            hymnal_title = "Christ in Song"
            hymnal_language = "English"
        elif isinstance(hymnal_data, dict) and "hymns" in hymnal_data:
            # It's an object with hymns array
            hymns = hymnal_data["hymns"]
            hymnal_title = hymnal_data.get("title", "Christ in Song")
            hymnal_language = hymnal_data.get("language", "English")
        else:
            logger.error("Unexpected JSON format")
            raise ValueError("Cannot parse hymnal data - unexpected format")

        hymn_count = len(hymns)

        logger.info(f"Hymnal: {hymnal_title}")
        logger.info(f"Language: {hymnal_language}")
        logger.info(f"Total hymns: {hymn_count}")
        print()

        # Confirm import
        response = input(
            f"This will import {hymn_count} hymns and clear existing data. Continue? (yes/no): "
        ).lower()
        if response not in ["yes", "y"]:
            logger.info("Import cancelled by user")
            return

        print()
        logger.info("Starting import...")

        # Import hymns
        import_hymns(db_manager, hymns)

        # Show final stats
        stats = db_manager.get_database_stats()
        print("\n📊 Database Statistics:")
        print(f"  • Total hymns: {stats['total_hymns']}")
        print(f"  • Total categories: {stats['total_categories']}")
        print(f"  • Database location: {db_manager.db_path}")
        print()

        # Create backup
        logger.info("Creating backup...")
        backup_path = db_manager.backup_database()
        if backup_path:
            print(f"✅ Backup created: {backup_path}")

        print("\n" + "=" * 70)
        print("✅ IMPORT COMPLETED SUCCESSFULLY!")
        print("=" * 70 + "\n")

        print("You can now run the application:")
        print("  python -m christ_in_song.main")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠️  Import cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Import failed: {e}", exc_info=True)
        print("\n❌ Import failed! Check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()