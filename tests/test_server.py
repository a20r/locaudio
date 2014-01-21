
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import time
import urllib
import urllib2
import json
import locaudio.db as db
import locaudio.api as api


server_addr = "10.0.0.221" #"192.168.1.9"
server_port = 8000

test_sound_name = "Cock"

loc = api.Locaudio(server_addr, server_port)

_, _, f_print = db.get_reference_data(test_sound_name)

d_dicts = [
    {
        "x": -9,
        "y": -1,
        "spl": 83,
        "timestamp": time.time(),
        "fingerprint": f_print
    },
    {
        "x": -2,
        "y": 1,
        "spl": 97,
        "timestamp": time.time() - 7,
        "fingerprint": f_print
    },
    {
        "x": 1,
        "y": 3,
        "spl": 86,
        "timestamp": time.time() - 10,
        "fingerprint": f_print
    },
    {
        "x": 0,
        "y": -1,
        "spl": 100,
        "timestamp": time.time() - 5,
        "fingerprint": f_print
    }
]


class ServerTest(unittest.TestCase):

    def test_server_notify(self):
        for d_dict in d_dicts:
            loc.notify_event(d_dict)

        print "\n=== Server Notify ===\n"


    def test_server_triangulation(self):
        pos_list = loc.get_sound_locations(test_sound_name)

        print "\n=== Server Triangulation === :: {0}\n".format(pos_list)


    def test_names(self):
        names_list = loc.get_names()

        print "\n=== Server Names === :: {0}\n".format(names_list)


if __name__ == "__main__":
    print "\n=== Server Testing ===\n"
    unittest.main()

