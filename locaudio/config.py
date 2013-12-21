
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

detection_events = list()
refresh_time = 10 # seconds

reference_print = None

position_list = list()
new_data = False

