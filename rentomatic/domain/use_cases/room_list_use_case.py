from typing import Union

from rentomatic.domain.interfaces.repository import Repository
from rentomatic.domain.request_objects import room_list_request_object as req
from rentomatic.domain.response_objects import response_objects as res
from rentomatic.domain.response_objects.response_objects import ResponseFailure, ResponseSuccess


class RoomListUseCase:
    def __init__(self, repo: Repository):
        self.repo = repo

    def execute(
        self, request_object: Union[req.ValidRequestObject, req.InvalidRequestObject]
    ) -> Union[ResponseSuccess, ResponseFailure]:
        if not request_object:
            return res.ResponseFailure.build_from_invalid_request_object(request_object)

        try:
            rooms = self.repo.list(filters=request_object.filters)
            return res.ResponseSuccess(rooms)
        except Exception as exc:
            return res.ResponseFailure.build_system_error("{}: {}".format(exc.__class__.__name__, "{}".format(exc)))
