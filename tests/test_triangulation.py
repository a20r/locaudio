
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import locaudio.triangulation as tri
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def testNormalizedEval():
    fig = plt.figure()
    ax = Axes3D(fig)
    dEvents = [
        tri.DetectionEvent(-1, -1, 0.9, 100),
        tri.DetectionEvent(-1, 1, 0.3, 90),
        tri.DetectionEvent(1, 1, 0.5, 100),
        tri.DetectionEvent(1, -1, 0.6, 100)
    ]

    lRef = 100
    rRef = 1

    x = y = np.arange(-10, 10, 0.05)
    X, Y = np.meshgrid(x, y)
    zs = np.array(
        [
            tri.normalizedEval(x, y, rRef, lRef, dEvents)
            for x, y in zip(np.ravel(X), np.ravel(Y))
        ]
    )
    Z = zs.reshape(X.shape)
    ax.plot_surface(X, Y, Z)
    plt.show()

    print tri.normalizedEval(0, 0, rRef, lRef, dEvents)

if __name__ == "__main__":
    testNormalizedEval()

