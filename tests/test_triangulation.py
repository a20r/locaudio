
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import locaudio.triangulation as tri
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.optimize as opt
import unittest


class TriangulationTest(unittest.TestCase):

    def __init__(self, *args):
        self.dEvents = [
            tri.DetectionEvent(-2, -1, 0.9, 90),
            tri.DetectionEvent(-1, 1, 0.3, 97),
            tri.DetectionEvent(2, 3, 0.5, 86),
            tri.DetectionEvent(1, -1, 0.6, 100)
        ]

        super(TriangulationTest, self).__init__(*args)

    def test_positionProbability(self):

        fig = plt.figure("Position Probability Test")
        ax = Axes3D(fig)
        ax.set_title("Sound location probability density function")
        ax.set_xlabel("X Location")
        ax.set_ylabel("Y Location")
        ax.set_zlabel("Probability")
        lRef = 100
        rRef = 1

        vMin = -10
        vMax = 10
        vStep = 0.05

        testX = 0
        testY = 0

        x = y = np.arange(vMin, vMax, vStep)
        X, Y = np.meshgrid(x, y)
        zs = np.array(
            [
                tri.positionProbability(x, y, rRef, lRef, self.dEvents)
                for x, y in zip(np.ravel(X), np.ravel(Y))
            ]
        )
        Z = zs.reshape(X.shape)
        ax.plot_surface(X, Y, Z)
        plt.show()

        print "\n=== Position Probability === ::", tri.positionProbability(
            testX, testY,
            rRef, lRef,
            self.dEvents
        ), "\n"


    def test_optimization(self):

        lRef = 100
        rRef = 1

        testX = 0
        testY = 0

        res = tri.determineSoundPosition(
            rRef, lRef,
            [testX, testY],
            self.dEvents
        )

        print "\n=== Optimization === ::", res, "\n"


if __name__ == "__main__":

    print "\n=== Triangulation Testing ===\n"
    unittest.main()


