
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

    def setUp(self):
        self.show_plot = True
        self.d_events = [
            tri.DetectionEvent(-3, -1, 0.9, 90),
            tri.DetectionEvent(-2, 1, 0.3, 97),
            tri.DetectionEvent(1, 3, 0.5, 86),
            tri.DetectionEvent(0, -1, 0.6, 100)
        ]


    def test_position_probability(self):

        l_ref = 100
        r_ref = 1

        test_x = 0
        test_y = 0

        if self.show_plot:
            fig = plt.figure("Position Probability Test")
            ax = Axes3D(fig)
            ax.set_title("Sound location probability density function")
            ax.set_xlabel("X Location")
            ax.set_ylabel("Y Location")
            ax.set_zlabel("Probability")

            v_min = -10
            v_max = 10
            v_step = 0.05

            x = y = np.arange(v_min, v_max, v_step)
            X, Y = np.meshgrid(x, y)
            zs = np.array(
                [
                    tri.position_probability(x, y, r_ref, l_ref, self.d_events)
                    for x, y in zip(np.ravel(X), np.ravel(Y))
                ]
            )
            Z = zs.reshape(X.shape)
            ax.plot_surface(X, Y, Z)
            plt.show()

        print "\n=== Position Probability === :: (", test_x,
        print ",", test_y , ")  --> ",
        print tri.position_probability(
            test_x, test_y,
            r_ref, l_ref,
            self.d_events
        ), "\n"


    def test_optimization(self):

        l_ref = 100
        r_ref = 1

        test_x = 0
        test_y = 0

        res = tri.determine_sound_position(
            r_ref, l_ref,
            [test_x, test_y],
            self.d_events,
            disp=0
        )

        print "\n=== Optimization === :: [ X, Y ]  <--> ", res, "\n"


if __name__ == "__main__":

    print "\n=== Triangulation Testing ===\n"
    unittest.main()

