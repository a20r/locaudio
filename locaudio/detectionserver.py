
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
    if config.reference_print == None:
        raise AttributeError("Reference print not yet defined")

    req_print = [int(x) for x in request.form["fingerprint"] if x.isdigit()]
    confidence = fingerprint.get_similarity(
        config.reference_print.fingerprint,
        req_print
    )

    if len(config.detection_events) + 1 >= MAX_NODE_EVENTS:
        del config.detection_events[0]

    config.detection_events.append(
        request_to_detection_event(request.form, confidence)
    )

    return jsonify(error=0, message="No error")


@config.app.route("/get_positions", methods=["GET"])
def get_sound_positions():
    if len(config.detection_events) == 0:
        return jsonify(error=1, message="No detection events yet")

    position_list = tri.determine_sound_positions(
        config.reference_print.radius,
        config.reference_print.spl,
        config.detection_events,
        disp=0
    )

    p_list = [p.to_list() for p in position_list]

    return jsonify(
        positions=p_list
    )


def run(host, port, reference_file):
    config.reference_print = fingerprint.load_fingerprint_from_file(
        reference_file
    )
    config.app.run(host=host, port=int(port), debug=True)

