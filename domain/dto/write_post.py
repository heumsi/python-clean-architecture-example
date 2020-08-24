from dataclasses import dataclass


@dataclass
class WritePostInputDto:
    author: str
    category: str
    content: str
    created_at: int
    updated_at: int


@dataclass
class WritePostOutputDto:
    is_success: bool
    error_message: str
