from typing import Union

from domain.dto.read_post import ReadPostOutputDto
from domain.entity.post import Post
from domain.exception.repository import NotExistedDataError
from domain.interface.post_repository import PostRepository


class ReadPost:
    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    def execute(self, post_id: int) -> Union[ReadPostOutputDto, None]:
        try:
            post: Post = self._repository.get_by_id(id=post_id)
        except NotExistedDataError:
            return None
        else:
            output_dto = ReadPostOutputDto(
                id=post.id,
                author=post.author,
                category=post.category,
                content=post.content,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            return output_dto
