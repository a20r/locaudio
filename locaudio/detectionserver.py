
from flask import request, jsonify, render_template
import time
import util
import config
import json
import triangulation as tri
import fingerprint
import db


MAX_NODE_EVENTS = 10
DEBUG = True
IMG_DIR = "imgs/"


def request_to_detection_event(req_dict, confidence):
    return tri.DetectionEvent(
        float(req_dict["x"]),
        float(req_dict["y"]),
        float(confidence),
        float(req_dict["spl"]),
        float(req_dict["timestamp"])
    )


@config.app.route("/notify", methods=["POST"])
def post_notify():
    req_print = [int(x) for x in request.form["fingerprint"] if x.isdigit()]

    sound_name, confidence = db.get_best_matching_print(
        req_print
    )

    if not sound_name in config.detection_events.keys():
        config.detection_events[sound_name] = list()

    if len(config.detection_events[sound_name]) + 1 >= MAX_NODE_EVENTS:
        del config.detection_events[sound_name][0]

    config.detection_events[sound_name].append(
        request_to_detection_event(request.form, confidence)
    )

    return jsonify(error=0, message="No error", name=sound_name)


@config.app.route("/positions/<sound_name>", methods=["GET"])
def get_sound_positions(sound_name):
    if not sound_name in config.detection_events.keys():
        return jsonify(error=1, message="No detection events yet")

    radius, spl = db.get_reference_data(sound_name)
    position_list = tri.determine_sound_positions(
        radius, spl,
        config.detection_events[sound_name],
        disp=0
    )

    prob_list = [
        tri.position_probability(
            p.x, p.y, radius, spl,
            config.detection_events[sound_name]
        ) for p in position_list
    ]

    ret_dict = list(
        {
            "position": p.to_list(),
            "confidence": conf
        } for p, conf in zip(position_list, prob_list)
    )

    return json.dumps(ret_dict)


@config.app.route("/viewer/<sound_name>", methods=["GET"])
def get_position_viewer(sound_name):
    if not sound_name in config.detection_events.keys():
        return render_template("graph.html")

    radius, spl = db.get_reference_data(sound_name)
    position_list = tri.determine_sound_positions(
        radius, spl,
        config.detection_events[sound_name],
        disp=0
    )

    img_path = IMG_DIR + util.getUUID() + ".png"

    tri.plot_detection_events(
        position_list,
        radius, spl,
        config.detection_events[sound_name],
        img_path
    )

    img_web_path = "/" + img_path

    r_template = render_template("graph.html", img_path=img_web_path)

    return r_template


