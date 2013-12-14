
"""

triangulation.py

This file contains functions that can be used to determine the position
of a sound in a mesh network given a set of nodeEvents with associated
information. The nodeEvent (at this point) is a simple struct containing
its x and y position, the confidence of the sound that was just detected,
and the sound pressure level of the sound when it was detected. Using this
information we can create a probability function that can be maximized to
determine the position of the sample sound. The sample sound (for localization
given that the sound has been accurately detected by a set of nodeEvents)
only needs to contain the reference sound pressure level and a reference
distance from which this measurement has been taken.

"""


from collections import namedtuple
from detectionevent import DetectionEvent
import math


# Scaling constant to transform a confidence probability into a
# a standard deviation.
K =  0.7


def distanceFromSound(rRef, lRef, l):
    """

    Determines the distance from a sound given the sound pressure level
    and a reference sound pressure level with an associated distance

    """

    return rRef * math.pow(10, (lRef - l) / 20)


def distanceFromDetectionEvent(x, y, nodeEvent):
    """

    Given x and y coordinates, this returns the distance to a nodeEvent
    where the nodeEvent has attributes, x and y, on the same plane

    """

    return math.sqrt(
        math.pow(x - nodeEvent.x, 2) +
        math.pow(y - nodeEvent.y, 2)
    )


def normalDistribution(x):
    """

    This is the normal distribution function

    """

    return (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * math.pow(x, 2))


def positionEvaluation(x, y, rRef, lRef, nodeEvents):
    """

    Evaluation function to deterimine with some weight, where a sound is
    located in the mesh network of nodes. Given an x and y, this returns
    a weight. The higher the weight, the higher the likelihood that the
    sound originated from x and y.

    """

    return sum(
        [
            normalDistribution(
                (
                    distanceFromDetectionEvent(x, y, n) -
                    distanceFromSound(rRef, lRef, n.spl)
                ) / (K / n.confidence)
            ) / (K / n.confidence) for n in nodeEvents
        ]
    )


def normalizedEval(x, y, rRef, lRef, nodeEvents):
    """

    Scales the evaluation function so it returns a probability (i.e. a float
    between 0 and 1 inclusive) that a given x and y is where a sample sound
    originated from

    """

    return positionEvaluation(
        x, y,
        rRef, lRef,
        nodeEvents
    ) / float(len(nodeEvents))


