
class DetectionEvent(object):
    """

    Class which is used to house the detection event. It is a persistent class
    which has variables x and y for position of the node when the event was
    registered, a confidence of sound recognition, and the sound pressure
    leve which can be used to determine the distance from the sound source.

    """

    def __init__(self, x, y, confidence, spl):
        self.x = x
        self.y = y
        self.confidence = confidence
        self.spl = spl


    def getX(self):
        return self.x


    def getY(self):
        return self.y


    def getConfidence(self):
        return self.confidence

    def getSPL(self):
        return self.spl

