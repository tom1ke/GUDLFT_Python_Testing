from datetime import datetime
from dataclasses import dataclass


@dataclass
class Competition:
    name: str
    date: datetime
    places: int
