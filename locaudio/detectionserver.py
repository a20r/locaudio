
from flask import request, jsonify
from util import run_thread
import time
import config
import json
import triangulation as tri
import fingerprint


def request_to_detection_event(req_dict, confidence):
    print confidence, type(confidence), "HERE"
    return tri.DetectionEvent(
        float(req_dict["x"]),
        float(req_dict["y"]),
        float(confidence),
        float(req_dict["spl"]),
        float(req_dict["timestamp"])
    )


def load_fingerprint_from_file(filename):
    with open(filename) as f:
        print_dict = json.loads(f.read())
        return fingerprint.ReferencePrint(
            print_dict["fingerprint"],
            print_dict["radius"],
            print_dict["sound_pressure_level"]
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

    config.detection_events.append(
        request_to_detection_event(request.form, confidence)
    )

    return jsonify(error=0, message="No error")


@config.app.route("/get_positions", methods=["GET"])
def get_sound_positions():
    ret_list = list()
    ret_list.extend(config.position_list)

    ret_bool = config.new_data
    config.new_data = False

    return jsonify(
        positions=map(lambda rl: rl.to_list(), ret_list),
        new_data=ret_bool
    )


@run_thread
def timer_thread():
    while True:
        if len(config.detection_events) > 0:
            time.sleep(config.refresh_time)
            config.position_list = tri.determine_sound_positions(
                config.reference_print.radius,
                config.reference_print.spl,
                config.detection_events,
                disp=0
            )

            config.new_data = True
            config.detection_events = list()


def run(host, port, reference_file):
    config.reference_print = load_fingerprint_from_file(reference_file)
    config.app.run(host=host, port=int(port), debug=True)

