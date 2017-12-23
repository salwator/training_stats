import numpy as np


def interpolate(points):
    time, values = zip(*points)
    new_time = np.arange(int(time[0]), int(time[-1]) + 1)
    return list(zip(new_time, np.interp(new_time, time, values)))
