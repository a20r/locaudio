
import triangulation as tri
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def determine_limits(*args):

    x_min = args[0][0].x
    x_max = args[0][0].x

    y_min = args[0][0].y
    y_max = args[0][0].y

    for coord_list in args:
        for coord in coord_list:
            if coord.x < x_min:
                x_min = coord.x
            elif coord.x > x_max:
                x_max = coord.x

            if coord.y < y_min:
                y_min = coord.y
            elif coord.y > y_max:
                y_max = coord.y

    if x_max - x_min > y_max - y_min:
        y_max = (x_max - x_min) + y_min
    else:
        x_max = (y_max - y_min) + x_min

    x_step = (x_max - x_min) / float(30)
    y_step = (y_max - y_min) / float(30)

    return (
        x_min - 100 * x_step, x_max + 100 * x_step,
        y_min - 100 * y_step, y_max + 100 * y_step,
        x_step, y_step
    )


def plot_detection_events(locations, r_ref, l_ref, d_events, filename):
    """

    Plots the detection events and saves the figure in the given path.

    @param res The list of locations. Locations are named tuples with fields
    which are position which is a point and confidence which is a float

    @param rRef The reference distance at which the reference sound
    pressure level was recorded

    @param lRef The reference sound pressure level used to determine the
    distance from the newly measured sound pressure level

    @param nodeEvents The list ofassociated data when a node detects with some
    confidence that the sound has been identified

    @return The plt object of the saved figure

    """

    fig = plt.figure("Locaudio")
    ax = fig.add_subplot(111)
    ax.set_xlabel("X Location")
    ax.set_ylabel("Y Location")

    # x_min = 56.3399
    # x_max = 56.3400
    # y_min = -2.80834
    # y_max = -2.80824

    (
        x_min, x_max,
        y_min, y_max,
        x_step, y_step
    ) = determine_limits(locations, d_events)

    x = np.arange(x_min, x_max, x_step)
    y = np.arange(y_min, y_max, y_step)
    X, Y = np.meshgrid(x, y)

    zs = np.array(
        [
            tri.position_probability(x, y, r_ref, l_ref, d_events)
            for x, y in zip(np.ravel(X), np.ravel(Y))
        ]
    )

    Z = zs.reshape(X.shape)
    ax.pcolormesh(X, Y, Z, cmap=cm.jet)
    ax.scatter(
        [p.position.x for p in locations],
        [p.position.y for p in locations],
        marker="+",
        linewidths=15,
        c="white"
    )
    ax.scatter(
        [d_event.x for d_event in d_events],
        [d_event.y for d_event in d_events],
        marker="o",
        linewidths=5,
        c="white",
        s=300
    )

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    plt.savefig(filename)
    return plt


