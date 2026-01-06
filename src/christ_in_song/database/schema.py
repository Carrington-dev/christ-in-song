"""
Database schema definitions for Christ In Song Hymnal
File: src/christ_in_song/database/schema.py
"""

# SQL schema for creating all database tables
SCHEMA = """
-- Categories table for organizing hymns
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Main hymns table
CREATE TABLE IF NOT EXISTS hymns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    verses TEXT NOT NULL,
    chorus TEXT,
    category_id INTEGER,
    author TEXT,
    composer TEXT,
    year INTEGER,
    copyright TEXT,
    scripture_reference TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Indexes for fast lookups
CREATE INDEX IF NOT EXISTS idx_hymn_number ON hymns(number);
CREATE INDEX IF NOT EXISTS idx_hymn_title ON hymns(title);
CREATE INDEX IF NOT EXISTS idx_hymn_category ON hymns(category_id);

-- Full-text search virtual table for searching hymns
CREATE VIRTUAL TABLE IF NOT EXISTS hymns_fts USING fts5(
    title, 
    verses, 
    author,
    composer,
    content=hymns,
    content_rowid=id
);

-- Triggers to keep FTS index in sync with hymns table
CREATE TRIGGER IF NOT EXISTS hymns_ai AFTER INSERT ON hymns BEGIN
    INSERT INTO hymns_fts(rowid, title, verses, author, composer)
    VALUES (new.id, new.title, new.verses, new.author, new.composer);
END;

CREATE TRIGGER IF NOT EXISTS hymns_ad AFTER DELETE ON hymns BEGIN
    DELETE FROM hymns_fts WHERE rowid = old.id;
END;

CREATE TRIGGER IF NOT EXISTS hymns_au AFTER UPDATE ON hymns BEGIN
    DELETE FROM hymns_fts WHERE rowid = old.id;
    INSERT INTO hymns_fts(rowid, title, verses, author, composer)
    VALUES (new.id, new.title, new.verses, new.author, new.composer);
END;

-- User favorites table
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hymn_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (hymn_id) REFERENCES hymns(id) ON DELETE CASCADE,
    UNIQUE(hymn_id)
);

-- Recently viewed hymns
CREATE TABLE IF NOT EXISTS recently_viewed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hymn_id INTEGER NOT NULL,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hymn_id) REFERENCES hymns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_recently_viewed_time ON recently_viewed(viewed_at DESC);

-- Application settings
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usage statistics for tracking popular hymns
CREATE TABLE IF NOT EXISTS usage_stats (
    hymn_id INTEGER PRIMARY KEY,
    view_count INTEGER DEFAULT 0,
    last_viewed TIMESTAMP,
    FOREIGN KEY (hymn_id) REFERENCES hymns(id) ON DELETE CASCADE
);

-- Database metadata
CREATE TABLE IF NOT EXISTS db_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial metadata
INSERT OR IGNORE INTO db_metadata (key, value) VALUES ('version', '1.0.0');
INSERT OR IGNORE INTO db_metadata (key, value) VALUES ('created_at', datetime('now'));
"""

# Default categories
DEFAULT_CATEGORIES = [
    ("Worship and Praise", "Hymns focused on worship and praise to God"),
    ("Prayer", "Hymns about prayer and communion with God"),
    ("Faith and Trust", "Hymns about faith, trust, and reliance on God"),
    ("Love of God", "Hymns celebrating God's love"),
    ("Salvation", "Hymns about salvation and redemption"),
    ("Second Coming", "Hymns about Christ's return"),
    ("Christian Life", "Hymns about daily Christian living"),
    ("Service", "Hymns about service to God and others"),
    ("Comfort and Peace", "Hymns offering comfort and peace"),
    ("Heaven", "Hymns about heaven and eternal life"),
    ("Gospel Invitation", "Hymns extending gospel invitation"),
    ("Testimony", "Hymns of personal testimony"),
    ("Nature", "Hymns about God's creation"),
    ("Christmas", "Christmas hymns"),
    ("Easter", "Easter hymns"),
    ("Special Occasions", "Hymns for special occasions"),
]

# Sample hymn data for testing
SAMPLE_HYMNS = [
    {
        "number": 1,
        "title": "Holy, Holy, Holy",
        "verses": """1. Holy, holy, holy! Lord God Almighty!
Early in the morning our song shall rise to Thee;
Holy, holy, holy! Merciful and mighty!
God in three Persons, blessèd Trinity!

2. Holy, holy, holy! All the saints adore Thee,
Casting down their golden crowns around the glassy sea;
Cherubim and seraphim falling down before Thee,
Which wert, and art, and evermore shalt be.

3. Holy, holy, holy! Though the darkness hide Thee,
Though the eye of sinful man Thy glory may not see,
Only Thou art holy; there is none beside Thee
Perfect in power, in love, and purity.

4. Holy, holy, holy! Lord God Almighty!
All Thy works shall praise Thy name in earth and sky and sea;
Holy, holy, holy! Merciful and mighty!
God in three Persons, blessèd Trinity!""",
        "chorus": None,
        "category": "Worship and Praise",
        "author": "Reginald Heber",
        "composer": "John B. Dykes",
        "year": 1826,
        "scripture_reference": "Revelation 4:8",
    },
    {
        "number": 2,
        "title": "Amazing Grace",
        "verses": """1. Amazing grace! How sweet the sound
That saved a wretch like me!
I once was lost, but now am found,
Was blind, but now I see.

2. 'Twas grace that taught my heart to fear,
And grace my fears relieved;
How precious did that grace appear
The hour I first believed!

3. Through many dangers, toils and snares,
I have already come;
'Tis grace hath brought me safe thus far,
And grace will lead me home.

4. When we've been there ten thousand years,
Bright shining as the sun,
We've no less days to sing God's praise
Than when we'd first begun.""",
        "chorus": None,
        "category": "Salvation",
        "author": "John Newton",
        "composer": "Traditional",
        "year": 1779,
        "scripture_reference": "Ephesians 2:8",
    },
    {
        "number": 3,
        "title": "What a Friend We Have in Jesus",
        "verses": """1. What a friend we have in Jesus,
All our sins and griefs to bear!
What a privilege to carry
Everything to God in prayer!
O what peace we often forfeit,
O what needless pain we bear,
All because we do not carry
Everything to God in prayer!

2. Have we trials and temptations?
Is there trouble anywhere?
We should never be discouraged;
Take it to the Lord in prayer.
Can we find a friend so faithful
Who will all our sorrows share?
Jesus knows our every weakness;
Take it to the Lord in prayer.

3. Are we weak and heavy laden,
Cumbered with a load of care?
Precious Savior, still our refuge,
Take it to the Lord in prayer.
Do thy friends despise, forsake thee?
Take it to the Lord in prayer!
In His arms He'll take and shield thee;
Thou wilt find a solace there.""",
        "chorus": None,
        "category": "Prayer",
        "author": "Joseph M. Scriven",
        "composer": "Charles C. Converse",
        "year": 1855,
        "scripture_reference": "John 15:15",
    },
]

# Default application settings
DEFAULT_SETTINGS = [
    ("theme", "light", "Application theme (light/dark)"),
    ("font_size", "12", "Default font size for hymn display"),
    ("show_hymn_numbers", "true", "Show hymn numbers in lists"),
    ("auto_backup", "true", "Automatic backup enabled"),
    ("backup_frequency", "7", "Backup frequency in days"),
    ("presentation_font_size", "24", "Font size for presentation mode"),
    ("recent_hymns_limit", "50", "Number of recent hymns to keep"),
]