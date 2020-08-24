from typing import List

from domain.dto.read_post import ReadPostOutputDto
from domain.entity.post import Post
from domain.interface.post_repository import PostRepository


class ReadPosts:
    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    def execute(self) -> List[ReadPostOutputDto]:
        posts: List[Post] = self._repository.get_all()

        return [
            ReadPostOutputDto(
                id=post.id,
                author=post.author,
                category=post.category,
                content=post.content,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            for post in posts
        ]
