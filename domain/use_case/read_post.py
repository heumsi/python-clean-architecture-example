import datetime
from dataclasses import dataclass
from typing import Union

from domain.entity.post import Post
from domain.exception.repository import NotExistedDataError
from domain.interface.post_repository import PostRepository


@dataclass
class ReadPostInputDto:
    post_id: int


@dataclass
class ReadPostOutputDto:
    post: Post


class ReadPost:
    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: ReadPostInputDto) -> Union[ReadPostOutputDto, None]:
        try:
            post: Post = self._repository.get_by_id(id=input_dto.post_id)
        except NotExistedDataError:
            return None
        else:
            output_dto = ReadPostOutputDto(post)
            return output_dto
