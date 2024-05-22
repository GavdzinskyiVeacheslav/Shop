from dataclasses import dataclass


@dataclass
class Order:
    id: int = 0
    name: str = ''
    description: str = ''


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
