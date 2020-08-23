from dataclasses import dataclass
from typing import List

from domain.entity.post import Post
from domain.interface.post_repository import PostRepository


@dataclass
class ReadPostsInputDto:
    pass


@dataclass
class ReadPostsOutputDto:
    posts: List[Post]


class ReadPosts:
    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: ReadPostsInputDto) -> ReadPostsOutputDto:
        posts: List[Post] = self._repository.get_all()
        output_dto = ReadPostsOutputDto(posts=posts)
        return output_dto
