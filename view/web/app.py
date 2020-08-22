from flask import Flask

from adapter.input_adapter import InputAdapter

app = Flask(__name__)

@app.route("/read_post/<int:post_id>/")
def read_post(post_id: int):
    InputAdapter()