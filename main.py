from typing import List, Union

from flask import Flask, abort, jsonify, request

from adapter.post_adapter import PostAdapter
from data.in_memory_post_repository import InMemoryPostRepository
from domain.dto.read_post import ReadPostOutputDto
from domain.dto.write_post import WritePostOutputDto
from domain.use_case.read_post import ReadPost
from domain.use_case.read_posts import ReadPosts
from domain.use_case.write_post import WritePost, WritePostInputDto

app = Flask(__name__)
repository = InMemoryPostRepository()


@app.route("/read_post/<int:post_id>/", methods=["GET"])
def read_post(post_id: int):
    # execute use_case
    use_case = ReadPost(repository=repository)
    output_dto: Union[ReadPostOutputDto, None] = use_case.execute(post_id=post_id)
    if output_dto is None:
        return abort(404, f"post_id = {post_id}")

    # convert output_dto to response_body
    response_body = PostAdapter.read_post_output_dto_to_response_body(output_dto)
    return jsonify(response_body)


@app.route("/read_posts/", methods=["GET"])
def read_posts():
    # execute use_case
    use_case = ReadPosts(repository=repository)
    output_dtos: List[ReadPostOutputDto] = use_case.execute()

    # convert output_dtos to response_body
    response_body = PostAdapter.read_post_output_dtos_to_response_body(output_dtos)
    return jsonify(response_body)


@app.route("/write_post/", methods=["POST"])
def write_post():
    # convert request_body to input_dto
    input_dto: WritePostInputDto = PostAdapter.request_body_to_write_post_input_dto(request.json)

    # execute use_case
    use_case = WritePost(repository=repository)
    output_dto: WritePostOutputDto = use_case.execute(input_dto=input_dto)

    # convert output_dto to response_body
    response_body = PostAdapter.write_post_output_dto_to_response_body(output_dto)

    return jsonify(response_body)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    app.run()
