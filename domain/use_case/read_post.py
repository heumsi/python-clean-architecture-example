from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from domain.repository.post_repository import PostRepository


@dataclass
class ReadPostInputDto:
    post_id: int


@dataclass
class ReadPostOutputDto:
    post_id: int
    author: str
    content: str
    created_at: str
    updated_at: str


class ReadPostOutputBoundary(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, output_dto: ReadPostOutputDto) -> None:
        pass


class ReadPostInputBoundary(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, input_dto: ReadPostInputDto, presenter: ReadPostOutputBoundary) -> None:
        pass


class ReadPost(ReadPostInputBoundary):
    """data 저장소에서 특정 글을 가져와 Presenter에게 전달한다.

    실행되는 순서는 다음과 같다.
        1. InputDto에 담긴 정보를 바탕으로 data 저장소에서 Post 데이터를 가져온다.
        2. 해당 Post 데이터를 바탕으로 OutputDto를 만든다.
        3. OutputDto 를 출력 레이어로 전달한다.
    """

    def __init__(self, repository: PostRepository):
        self._repository = repository

    def execute(self, input_dto: ReadPostInputDto, output_boundary: ReadPostOutputBoundary) -> None:
        post = self._repository.get_post_by_id(id=input_dto.post_id)
        output_dto = ReadPostOutputDto(
            post_id=post.id,
            author=post.author,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
        output_boundary.present(output_dto)