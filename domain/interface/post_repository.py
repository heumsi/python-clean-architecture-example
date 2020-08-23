from abc import ABCMeta, abstractmethod
from typing import List, Union

from domain.entity.post import Post


class PostRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_by_id(self, id: int) -> Union[Post, None]:
        pass

    @abstractmethod
    def get_all(self) -> List[Post]:
        pass

    @abstractmethod
    def save(self, post: Post) -> bool:
        pass
