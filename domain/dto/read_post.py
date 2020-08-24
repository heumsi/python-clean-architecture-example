import datetime
from dataclasses import dataclass


@dataclass
class ReadPostOutputDto:
    id: int
    author: str
    category: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
