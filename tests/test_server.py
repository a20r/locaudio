
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
import socket


server_addr = socket.gethostbyname(socket.getfqdn())
server_port = 8000

test_sound_class = "Chicken"
test_sound_name = "Cock"

loc = api.Locaudio(server_addr, server_port)

_, _, f_print = db.get_reference_data(test_sound_name)

d_dicts = [
    {
        "x": 56.3399723,
        "y": -2.8082881,
        "spl": 65,
        "timestamp": time.time() - 3,
        "fingerprint": f_print
    },
    {
        "x": 56.3399723,
        "y": -2.8082881,
        "spl": 65,
        "timestamp": time.time() - 1,
        "fingerprint": f_print
    },
    {
        "x": 56.3399723,
        "y": -2.8082881,
        "spl": 65,
        "timestamp": time.time() - 5,
        "fingerprint": f_print
    },
    {
        "x": 56.3399723,
        "y": -2.8082881,
        "spl": 65,
        "timestamp": time.time(),
        "fingerprint": f_print
    }
]


class ServerTest(unittest.TestCase):

    def test_server_notify_added(self):
        for d_dict in d_dicts:
            ret_dict = loc.notify_event(d_dict)

        print "\n=== Server Notify Added === :: {0}\n".format(ret_dict)


    def test_server_notify_not_added(self):
        for d_dict in d_dicts:
            d_dict["fingerprint"] = [1, 2, 3, 4]
            ret_dict = loc.notify_event(d_dict)

        print "\n=== Server Notify Not Added === :: {0}\n".format(ret_dict)


    def test_server_sound_triangulation(self):
        pos_list = loc.get_sound_locations(test_sound_name)

        print "\n=== Server Sound Triangulation === :: {0}\n".format(pos_list)


    def test_server_sound_class_triangulation(self):
        pos_list = loc.get_class_locations(test_sound_class)

        print "\n=== Server Class Triangulation === :: {0}\n".format(pos_list)


    def test_names(self):
        names_list = loc.get_names()

        print "\n=== Server Names === :: {0}\n".format(names_list)


if __name__ == "__main__":
    print "\n=== Server Testing ===\n"
    unittest.main()

