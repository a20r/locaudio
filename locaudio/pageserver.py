
import config
from flask import Response, jsonify, render_template
import db
import util
import os

MIME_DICT = {
    "js": "text/javascript",
    "css": "text/css",
    "imgs": "image/png",
    "libraries": "text/javascript",
    "data": "text/csv",
    "sounds":  "audio/vnd.wav"
}


@config.app.route("/<file_type>/<filename>", methods=["GET"])
def get_static(file_type, filename):
    with open(file_type + "/" + filename) as f:
        res = Response(f.read(), mimetype=MIME_DICT[file_type])
        return res


@config.app.route("/", methods=["GET"])
def get_index():
    names = db.get_list_of_names()
    number_of_events = [
        len(util.try_get(config.detection_events, name))
        for name in names
    ]

    return render_template(
        "index.html",
        name_data=zip(names, number_of_events)
    )

