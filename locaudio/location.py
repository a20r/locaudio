
import json


class Location(object):

    def __init__(self, position, confidence):
        self.position = position
        self.x = position.x
        self.y = position.y
        self.confidence = confidence


    def get_position(self):
        return self.position


    def get_confidence(self):
        return self.confidence


    def set_position(self, position):
        self.position = position
        return self


    def set_confidence(self, confidence):
        self.confidence = confidence
        return self


    def to_dict(self):
        return {
            "position": {
                "x": self.position.x,
                "y": self.position.y
            },
            "confidence": self.confidence
        }


    def to_json(self):
        return json.dumps(self.to_dict())


    def __hash__(self):
        return hash(repr(self))


    def __eq__(self, other_location):
        attrs = ["x", "y", "confidence"]

        for attr in attrs:
            if not hasattr(other_location, attr):
                return False

            if not getattr(self, attr) == getattr(other_location, attr):
                return False

        return True


    def __repr__(self):
        return "Location(position={0}, confidence={1})".format(
            repr(self.position), self.confidence
        )
