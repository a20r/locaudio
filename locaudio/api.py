
import urllib
import urllib2
import json
import time


class Locaudio:

    def __init__(self, host, port):
        self.url = "http://" + host + ":" + str(port)
        self.pos_url = self.url + "/get_positions"
        self.notify_url = self.url + "/notify"
        self.sleep_time = 0.1


    def get_sound_positions_no_block(self):
        req = urllib2.urlopen(self.pos_url)
        data = json.loads(req.read())
        return data["positions"], data["new_data"]


    def get_sound_positions(self):
        while True:
            time.sleep(self.sleep_time)
            pos_list, new_data = self.get_sound_positions_no_block()

            if new_data:
                return pos_list


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


