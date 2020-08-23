import datetime
import json
from dataclasses import asdict, is_dataclass
from typing import Union

from flask import Flask, abort, jsonify, request

from data.in_memory_post_repository import InMemoryPostRepository
from domain.use_case.read_post import (ReadPost, ReadPostInputDto,
                                       ReadPostOutputDto)
from domain.use_case.read_posts import (ReadPosts, ReadPostsInputDto,
                                        ReadPostsOutputDto)
from domain.use_case.write_post import WritePost, WritePostInputDto

app = Flask(__name__)
repository = InMemoryPostRepository()


@app.route("/read_post/<int:post_id>/", methods=["GET"])
def read_post(post_id: int):
    # convert json to dto
    input_dto = ReadPostInputDto(post_id=post_id)

    # execute use_case
    use_case = ReadPost(repository=repository)
    output_dto: Union[ReadPostOutputDto, None] = use_case.execute(input_dto=input_dto)
    if output_dto is None:
        response_body = abort(404, description="Resource not found")

    # convert dto to json
    response_data = json.dumps(asdict(output_dto), default=_default_json_encoder)

    return jsonify(response_data)


@app.route("/read_posts/", methods=["GET"])
def read_posts():
    # convert json to dto
    input_dto = ReadPostsInputDto()

    # execute use_case
    use_case = ReadPosts(repository=repository)
    output_dto: ReadPostsOutputDto = use_case.execute(input_dto=input_dto)

    # convert dto to json
    response_data = json.dumps(asdict(output_dto), default=_default_json_encoder)

    return jsonify(response_data)


@app.route("/write_post/", methods=["POST"])
def write_post():
    # convert json to dto
    data = request.json
    input_dto = WritePostInputDto(**data)

    # execute use_case
    use_case = WritePost(repository=repository)
    output_dto = use_case.execute(input_dto=input_dto)

    # convert dto to json
    response_data = json.dumps(asdict(output_dto), default=_default_json_encoder)

    return jsonify(response_data)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


def _default_json_encoder(obj: object):
    if is_dataclass(obj):
        return asdict(obj)
    elif isinstance(obj, datetime.datetime):
        return obj.timestamp()
    else:
        return repr(obj)


if __name__ == "__main__":
    app.run()
