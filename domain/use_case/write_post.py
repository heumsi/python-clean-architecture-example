from dataclasses import dataclass

from domain.entity.post import Post
from domain.interface.post_repository import PostRepository


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


class WritePost:
    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: WritePostInputDto) -> WritePostOutputDto:
        post = Post(
            id=None,
            author=input_dto.author,
            category=input_dto.category,
            content=input_dto.content,
            created_at=input_dto.created_at,
            updated_at=input_dto.updated_at,
        )
        is_success: bool = self._repository.save(post)
        output_dto = WritePostOutputDto(is_success=is_success)
        return output_dto
