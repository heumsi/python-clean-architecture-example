from abc import ABCMeta, abstractmethod

from domain.entity.post import Post

class PostRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_post_by_id(self, id: int) -> Post:
        pass