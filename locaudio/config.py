
from flask import Flask
import db

app = Flask(__name__)
app.config.from_object(__name__)

detection_events = dict()
new_data = dict()

# So the routes get initiated
import detectionserver
import pageserver


def run(host, port):
    """

    Runs the server.

    @param host The host for the server

    @param port The port for the server

    """

    db.init()
    app.run(host=host, port=int(port), debug=True)



