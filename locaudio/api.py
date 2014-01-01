
import urllib
import urllib2
import json
import time


class Locaudio:

    def __init__(self, host, port):
        self.url = "http://" + host + ":" + str(port)
        self.pos_url = self.url + "/positions"
        self.notify_url = self.url + "/notify"


    def make_position_url(self, sound_name):
        return self.pos_url + "/" + sound_name


    def get_sound_positions(self, sound_name):
        req = urllib2.urlopen(self.make_position_url(sound_name))
        data = json.loads(req.read())
        return data["positions"]


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


