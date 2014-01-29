
import math


EARTH_RADIUS = 1000 * 6371


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def get_x(self):
        return self.x


    def get_y(self):
        return self.y


    def set_x(self, x):
        self.x = x
        return self


    def set_y(self, y):
        self.y = y
        return self


    def dist_to(self, other_point):
        return math.sqrt(
            pow(self.x - other_point.x, 2) +
            pow(self.y - other_point.y, 2)
        )


    def dist_to_lat_long(self, other_point):
        lat1 = math.radians(self.x)
        lon1 = math.radians(self.y)
        lat2 = math.radians(other_point.x)
        lon2 = math.radians(other_point.y)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = (
            (math.sin(dlat / 2)) ** 2 +
            math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2)) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = EARTH_RADIUS * c

        return distance


    def to_list(self):
        return [self.x, self.y]


    def __str__(self):
        return "X: {0}, Y: {1}".format(self.x, self.y)


    def __repr__(self):
        return "Point({0}, {1})".format(self.x, self.y)


