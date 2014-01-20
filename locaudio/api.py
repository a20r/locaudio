
import urllib
import urllib2
import json
import time
from location import Location
from point import Point


class Locaudio:

    def __init__(self, host, port):
        self.url = "http://" + host + ":" + str(port)
        self.pos_url = self.url + "/locations"
        self.notify_url = self.url + "/notify"
        self.names_url = self.url + "/names"


    def make_position_url(self, sound_name):
        return self.pos_url + "/" + sound_name


    def get_sound_locations(self, sound_name):
        req = urllib2.urlopen(self.make_position_url(sound_name))
        location_list = json.loads(req.read())
        ret_list = list()

        for location in location_list:
            position = Point(
                location["position"]["x"],
                location["position"]["y"]
            )

            ret_list.append(
                Location(position, location["confidence"])
            )

        return ret_list


    def get_names(self):
        req = urllib2.urlopen(self.names_url)
        names_dict = json.loads(req.read())
        return names_dict["names"]


    def notify_event(self, data):

        encdata = urllib.urlencode(data)

        hdr = {
            "Accept":
                "text/html,application/xhtml+xml," +
                "application/xml;q=0.9,*/*;q=0.8",
        }

        req = urllib2.Request(url=self.notify_url, data=encdata)
        res = urllib2.urlopen(req)
        return res.read()


