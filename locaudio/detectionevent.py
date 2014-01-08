
class DetectionEvent(object):
    """

    Class which is used to house the detection event. It is a persistent class
    which has variables x and y for position of the node when the event was
    registered, a confidence of sound recognition, and the sound pressure
    leve which can be used to determine the distance from the sound source.

    """


    def __init__(self, x, y, confidence, spl, timestamp):
        self.x = x
        self.y = y
        self.confidence = confidence
        self.spl = spl
        self.timestamp = timestamp
        self.std = None


    def get_x(self):
        return self.x


    def get_y(self):
        return self.y


    def get_confidence(self):
        return self.confidence


    def get_spl(self):
        return self.spl


    def get_timestamp(self):
        return self.timestamp


    def get_pos(self):
        return [self.x, self.y]


    def set_std(self, std):
        self.std = std


    def get_std(self):
        if self.std == None:
            raise AttributeError("Standard deviation not set")
        else:
            return self.std


    def __str__(self):
        return (
            "DetectionEvent(x=" + str(self.x) +
            ", y=" + str(self.y) +
            ", confidence=" + str(self.confidence) +
            ", spl=" + str(self.spl) + ")"
        )


    def __repr__(self):
        return self.__str__()

