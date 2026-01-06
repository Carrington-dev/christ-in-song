"""
Database models and data classes for Christ In Song Hymnal
File: src/christ_in_song/database/models.py
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Hymn:
    """Hymn data model"""

    id: int
    number: int
    title: str
    verses: str
    chorus: Optional[str] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    author: Optional[str] = None
    composer: Optional[str] = None
    year: Optional[int] = None
    copyright: Optional[str] = None
    scripture_reference: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Hymn":
        """Create a Hymn instance from a dictionary"""
        return cls(
            id=data.get("id"),
            number=data.get("number"),
            title=data.get("title"),
            verses=data.get("verses"),
            chorus=data.get("chorus"),
            category_id=data.get("category_id"),
            category_name=data.get("category_name"),
            author=data.get("author"),
            composer=data.get("composer"),
            year=data.get("year"),
            copyright=data.get("copyright"),
            scripture_reference=data.get("scripture_reference"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def get_verse_list(self) -> list:
        """Split verses into a list"""
        return [v.strip() for v in self.verses.split("\n\n") if v.strip()]

    def get_full_text(self) -> str:
        """Get the full text of the hymn including chorus"""
        text = self.verses
        if self.chorus:
            text += "\n\nChorus:\n" + self.chorus
        return text


@dataclass
class Category:
    """Category data model"""

    id: int
    name: str
    description: Optional[str] = None
    hymn_count: int = 0
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """Create a Category instance from a dictionary"""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            hymn_count=data.get("hymn_count", 0),
            created_at=data.get("created_at"),
        )


@dataclass
class Favorite:
    """Favorite hymn data model"""

    id: int
    hymn_id: int
    hymn: Optional[Hymn] = None
    added_at: Optional[datetime] = None
    notes: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Favorite":
        """Create a Favorite instance from a dictionary"""
        return cls(
            id=data.get("id"),
            hymn_id=data.get("hymn_id"),
            added_at=data.get("added_at"),
            notes=data.get("notes"),
        )


@dataclass
class RecentlyViewed:
    """Recently viewed hymn data model"""

    id: int
    hymn_id: int
    hymn: Optional[Hymn] = None
    viewed_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "RecentlyViewed":
        """Create a RecentlyViewed instance from a dictionary"""
        return cls(
            id=data.get("id"),
            hymn_id=data.get("hymn_id"),
            viewed_at=data.get("viewed_at"),
        )


@dataclass
class UsageStat:
    """Usage statistics data model"""

    hymn_id: int
    view_count: int = 0
    last_viewed: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> "UsageStat":
        """Create a UsageStat instance from a dictionary"""
        return cls(
            hymn_id=data.get("hymn_id"),
            view_count=data.get("view_count", 0),
            last_viewed=data.get("last_viewed"),
        )