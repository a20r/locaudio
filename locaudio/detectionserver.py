
from flask import Flask, request

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/notify", methods=["POST"])
def post_notify():
    pass


