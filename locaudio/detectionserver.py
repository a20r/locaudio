
from flask import request, jsonify
import time
import util
import config
import json
import triangulation as tri
import fingerprint
import db


MAX_NODE_EVENTS = 100


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


@config.app.route("/get_positions/<sound_name>", methods=["GET"])
def get_sound_positions(sound_name):
    if not sound_name in config.detection_events.keys():
        return jsonify(error=1, message="No detection events yet")

    radius, spl = db.get_reference_data(sound_name)

    position_list = tri.determine_sound_positions(
        radius, spl,
        config.detection_events[sound_name],
        disp=0
    )

    p_list = [p.to_list() for p in position_list]

    return jsonify(positions=p_list)


def run(host, port, reference_file):
    config.reference_print = fingerprint.load_fingerprint_from_file(
        reference_file
    )
    config.app.run(host=host, port=int(port), debug=True)

