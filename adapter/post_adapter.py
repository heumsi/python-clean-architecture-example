import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, List

from domain.dto.read_post import ReadPostOutputDto
from domain.dto.write_post import WritePostInputDto, WritePostOutputDto


class PostAdapter:
    @classmethod
    def read_post_output_dto_to_response_body(cls, read_post_output_dto: ReadPostOutputDto) -> str:
        return json.dumps(asdict(read_post_output_dto), default=cls._default_json_encoder)

    @classmethod
    def read_post_output_dtos_to_response_body(cls, read_post_output_dtos: List[ReadPostOutputDto]) -> str:
        return json.dumps(
            [asdict(output_dtos) for output_dtos in read_post_output_dtos], default=cls._default_json_encoder
        )

    @classmethod
    def request_body_to_write_post_input_dto(cls, request_body: dict) -> WritePostInputDto:
        return WritePostInputDto(**request_body)

    @classmethod
    def write_post_output_dto_to_response_body(cls, write_post_output_dto: WritePostOutputDto) -> str:
        return json.dumps(asdict(write_post_output_dto), default=cls._default_json_encoder)

    @staticmethod
    def _default_json_encoder(obj: object) -> Any:
        if is_dataclass(obj):
            return asdict(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.timestamp()
        else:
            return repr(obj)
