
__author__ = "Alexander Wallar <aw204@st-andrews.ac.uk>"


"""

@package Locaudio

Package contains code for sound source localization in reconfigurable
wireless acoustic sensor networks

"""


def run(host, port, config_filename):
    """

    Runs the server.

    @param host The host for the server

    @param port The port for the server

    """

    import config
    config.load_config_file(config_filename)

    global triangulation, detectionserver, fingerprint

    import triangulation
    import detectionserver
    import fingerprint

    import db
    import detectionserver
    import pageserver

    db.init()
    config.app.run(host=host, port=int(port), debug=True)


