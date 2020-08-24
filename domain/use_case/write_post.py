from domain.dto.write_post import WritePostInputDto, WritePostOutputDto
from domain.entity.post import Post
from domain.interface.post_repository import PostRepository


class WritePost:
    def __init__(self, repository: PostRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: WritePostInputDto) -> WritePostOutputDto:
        post = Post(
            id=None,  # this will be injected by repository.
            author=input_dto.author,
            category=input_dto.category,
            content=input_dto.content,
            created_at=input_dto.created_at,
            updated_at=input_dto.updated_at,
        )
        try:
            self._repository.save(post)
        except Exception as err:
            return WritePostOutputDto(is_success=False, error_message=str(err))
        else:
            return WritePostOutputDto(is_success=True, error_message="")
