
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import time
import urllib
import urllib2
import json
import locaudio.api as api


server_addr = "localhost"
server_port = 8000

loc = api.Locaudio(server_addr, server_port)

d_dicts = [
    {
        "x": -9,
        "y": -1,
        "spl": 90,
        "timestamp": time.time(),
        "fingerprint": [1,2,3,4]
    },
    {
        "x": -2,
        "y": 1,
        "spl": 97,
        "timestamp": time.time() - 7,
        "fingerprint": [1,2,3,4]
    },
    {
        "x": 1,
        "y": 3,
        "spl": 86,
        "timestamp": time.time() - 10,
        "fingerprint": [1,2,3,4]
    },
    {
        "x": 0,
        "y": -1,
        "spl": 100,
        "timestamp": time.time() - 5,
        "fingerprint": [1,2,3,4]
    }
]


class ServerTest(unittest.TestCase):

    def test_server_notify(self):
        for d_dict in d_dicts:
            loc.notify_event(d_dict)

        print "\n=== Server Notify ===\n"


    def test_server_triangulation(self):
        pos_list = loc.get_sound_positions()

        print "\n=== Server Triangulation === :: {0}\n".format(pos_list)


if __name__ == "__main__":
    print "\n=== Server Testing ===\n"
    unittest.main()

