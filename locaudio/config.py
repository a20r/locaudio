
import json
import sys

from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

detection_events = dict()
class_detection_events = dict()
new_data = dict()

this = sys.modules[__name__]

# setting default values
jvm_path = "/System/Library/Frameworks/JavaVM.framework/JavaVM"
db_host = "localhost"
db_port = 28015
max_node_events = 10
min_confidence = 0.3
debug_mode = True


def load_config_file(filename):
    global this
    with open(filename) as f:
        config_dict = json.loads(f.read())
        for config_key, config_value in config_dict.items():
            setattr(this, config_key, config_value)


