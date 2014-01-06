
from flask import Flask
import db

app = Flask(__name__)
app.config.from_object(__name__)

detection_events = dict()

position_list = list()


# So the routes get initiated
import detectionserver
import pageserver


def run(host, port):
    db.init()
    app.run(host=host, port=int(port), debug=True)



