#!/usr/bin/env python3

import sys
from operator import itemgetter
from datetime import datetime
import xml.etree.cElementTree as ET
import matplotlib.pyplot as pyplot
import numpy as np
import re


def get_time(trkpt, namespace):
    time_children = trkpt.find("./{0}time".format(namespace))
    if time_children is not None:
        return time_children.text


def get_hr(trkpt, namespace):
    extension_children = trkpt.find('./{0}extensions/./'.format(namespace))
    ext_ns = re.match('\{.*\}', extension_children.tag).group(0)
    hr_child = extension_children.find('./{0}hr'.format(ext_ns))
    if hr_child is not None:
        return int(hr_child.text)


def decode_iso_time(timestr):
    return datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%SZ')


def convert_time(time, start):
    """ Calculates elapsed timed from start in second """
    dt = decode_iso_time(time) - start
    return int(dt.total_seconds())


def get_trkpts(gpx_file):
    tree = ET.parse(gpx_file)
    root = tree.getroot()
    ns = re.match('\{.*\}', root.tag).group(0)
    return (ns, root.findall('./{0}trk/{0}trkseg/{0}trkpt'.format(ns)))


def get_hr_measurements(gpx_file):
    """ Generates list of (t, hr) from gpx. Skips missing measuruments. """
    ns, trkpts = get_trkpts(gpx_file)
    data = [(get_time(p, ns), get_hr(p, ns)) for p in trkpts]
    start_time = decode_iso_time(data[0][0])
    return [(convert_time(t, start_time), hr) for (t, hr) in data if hr]


def interpolate(points):
    time, hr = zip(*points)
    new_time = np.arange(int(time[-1]))
    return list(zip(new_time, np.interp(new_time, time, hr)))


def calculate_moving_sums(points, window):
    """ Calculates hr moving sums of the window len """
    time, hrs = zip(*points)
    moving_sum = sum(hrs[0:window])
    sums = [(time[0], moving_sum)]
    for i, t in enumerate(time[1:-1 * window]):
        moving_sum += hrs[i + window] - hrs[i]
        sums.append((t, moving_sum))
    return sums


def main():
    test_period = 60 * 30      # test time
    measured_period = 60 * 20  # measured period in seconds
    plot_hr = False            # turn off to disable data plotting

    gpx_file = sys.argv[1]
    print("Loading gpx: {}".format(gpx_file))

    hrs = interpolate(get_hr_measurements(gpx_file))
    time_stamp, max_sum = max(calculate_moving_sums(hrs, test_period),
                              key=itemgetter(1))

    # your lactate threshold is average of last 20 in 30 minutes of tempo run
    start_measure = time_stamp + (test_period - measured_period)
    stop_measure = start_measure + measured_period
    measured_time, measured_hrs = zip(*hrs[start_measure:stop_measure])
    lactate_thr = round(sum(measured_hrs) / measured_period)

    print("Your lactate threshold is {} bpm.".format(lactate_thr))

    if(plot_hr):
        t, hr = zip(*hrs)
        pyplot.plot(t, hr, 'b')
        pyplot.plot(measured_time, measured_hrs, 'r')
        pyplot.show()


if __name__ == "__main__":
    main()
