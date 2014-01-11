
from flask import request, jsonify, render_template
import time
import util
import config
import json
import triangulation as tri
import fingerprint
import db
import os


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
    req_print = json.loads(request.form["fingerprint"])

    sound_name, confidence = db.get_best_matching_print(req_print)

    if not sound_name in config.detection_events.keys():
        config.detection_events[sound_name] = list()

    config.new_data[sound_name] = True

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

    radius, spl, _ = db.get_reference_data(sound_name)
    location_list = tri.determine_sound_positions(
        radius, spl,
        config.detection_events[sound_name],
        disp=0
    )

    for location in location_list:
        location["position"] = {
            "x": location["position"].x,
            "y": location["position"].y
        }

    return json.dumps(location_list)


@config.app.route("/viewer/<sound_name>", methods=["GET"])
def get_position_viewer(sound_name):
    if not sound_name in config.detection_events.keys():
        return render_template("graph.html", sound_name=sound_name)

    radius, spl, _ = db.get_reference_data(sound_name)
    location_list = tri.determine_sound_positions(
        radius, spl,
        config.detection_events[sound_name],
        disp=0
    )

    img_path = IMG_DIR + sound_name + ".png"

    if config.new_data[sound_name]:
        tri.plot_detection_events(
            location_list,
            radius, spl,
            config.detection_events[sound_name],
            img_path
        )

        config.new_data[sound_name] = False

    img_web_path = "/" + img_path

    for location in location_list:
        location["confidence"] = round(location["confidence"], 3)
        location["position"].x = round(location["position"].x, 3)
        location["position"].y = round(location["position"].y, 3)

    r_template = render_template(
        "graph.html",
        img_path=img_web_path,
        location_list=location_list,
        sound_name=sound_name,
        detection_events=config.detection_events[sound_name],
        r_ref=radius,
        l_ref=spl
    )

    return r_template


@config.app.route("/upload", methods=["GET", "POST"])
def get_post_upload():
    file_key = "sound_file"
    upload_folder = "sounds"
    if request.method == "POST" and file_key in request.files:
        sound_file = request.files[file_key]
        file_path = os.path.join(
            upload_folder,
            request.form["sound_name"] + ".wav"
        )

        sound_file.save(file_path)
        db.insert_reference(
            request.form["sound_name"],
            fingerprint.get_fingerprint(file_path),
            float(request.form["r_ref"]),
            float(request.form["l_ref"])
        )
    return render_template("upload.html")


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


@config.app.route("/names", methods=["GET"])
def get_sound_names():
    return jsonify(names=db.get_list_of_names())


