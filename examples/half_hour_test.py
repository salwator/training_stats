#!/usr/bin/env python3

import sys
from operator import itemgetter
import matplotlib.pyplot as pyplot
from .gpxfile import get_hr_measurements, interpolate


def calculate_moving_sums(points, window):
    """ Calculates hr moving sums of the window len """
    time, hrs = zip(*points)
    moving_sum = sum(hrs[0:window])
    sums = [(time[0], moving_sum)]
    for i, t in enumerate(time[1:-1 * window]):
        moving_sum += hrs[i + window] - hrs[i]
        sums.append((t, moving_sum))
    return sums



def calculate_lactate_threshold(hrdata):
    """ Given list of (time, hr), returns lactate threshold and selected data"""
    test_period = 60 * 30      # test time
    measured_period = 60 * 20  # measured period in seconds
    hrs = interpolate(hrdata)
    time_stamp, max_sum = max(calculate_moving_sums(hrs, test_period),
                              key=itemgetter(1))
    
    # your lactate threshold is average of last 20 in 30 minutes of tempo run
    start_measure = time_stamp + (test_period - measured_period)
    stop_measure = start_measure + measured_period
    measured_time, measured_hrs = zip(*hrs[start_measure:stop_measure])
    lactate_thr = round(sum(measured_hrs) / measured_period) 
    return (lactate_thr, measured_time, measured_hrs)


def main():
    plot_hr = False  # turn off to disable data plotting

    gpx_file = sys.argv[1] 
    print("Loading gpx: {}".format(gpx_file))

    hrdata = get_hr_measurements(gpx_file)
    lactate_thr, measured_time, measured_hrs = calculate_lactate_threshold(hrdata)

    print("Your lactate threshold is {} bpm.".format(lactate_thr))
    if(plot_hr):
        print('Plotting training data')
        t, hr = zip(*hrdata)
        pyplot.plot(t, hr, 'b')
        pyplot.plot(measured_time, measured_hrs, 'r')
        pyplot.xlabel('Time [s]')
        pyplot.ylabel('Hart rate [bpm]')
        pyplot.show()


if __name__ == "__main__":
    main()
