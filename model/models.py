from dataclasses import dataclass
from datetime import datetime


@dataclass
class Category:
    id: int = 0
    name: str = ''
    description: str = ''
    folder: str = ''


@dataclass
class Section:
    id: int = 0
    name: str = ''
    category_id: int = 0
    description: str = ''
    folder: str = ''


@dataclass
class Good:
    id: int = 0
    category_id: int = 0
    section_id: int = 0
    add_date: datetime = datetime.now()
    name: str = ''
    description: str = ''
    price: float = 0.0
    existence: int = 0


@dataclass
class Photo:
    id: int = 0
    good_id: int = 0
    width: int = 0
    height: int = 0
