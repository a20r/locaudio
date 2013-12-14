
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import locaudio.triangulation as tri
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import unittest


class TriangulationTest(unittest.TestCase):

    def setUp(self):
        print ""
        print "=== Triangulation Testing ===\n"
        self.dEvents = [
            tri.DetectionEvent(-1, -1, 0.9, 100),
            tri.DetectionEvent(-1, 1, 0.3, 90),
            tri.DetectionEvent(1, 1, 0.5, 100),
            tri.DetectionEvent(1, -1, 0.6, 100)
        ]

    def test_positionProbability(self):

        print "=== Position Probability === ::",
        fig = plt.figure()
        ax = Axes3D(fig)

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

        print tri.positionProbability(testX, testY, rRef, lRef, self.dEvents)

if __name__ == "__main__":
    unittest.main()

