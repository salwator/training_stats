#!/usr/bin/env python3


from xml.dom.minidom import parse
from operator import itemgetter
import matplotlib.pyplot as pyplot
from datetime import timedelta, datetime
import sys

# assume sampling time is 1s
measured_window = 60 * 20

# set off to disable plotting
plot_hr = True


def get_hr_measurements(gpx_file):
    gpx = parse(gpx_file)
    return [int(hr.childNodes[0].wholeText)
            for hr in gpx.getElementsByTagName('gpxtpx:hr')]

def calculate_moving_sums(measures, windowlen):
    limit = len(measures) - windowlen
    return [(time_point, sum(measures[time_point:time_point+windowlen]))
            for time_point in range(0, limit)]

def get_trkpts(gpx_file):
    gpx = parse(gpx_file)
    return gpx.childNodes[0].getElementsByTagName("trkpt")

def get_time(trkpt):
    return trkpt.getElementsByTagName("time")[0].childNodes[0].toxml()

def get_hr(trkpt):
    return int(trkpt.getElementsByTagName('gpxtpx:hr')[0].childNodes[0].wholeText)


gpx_file = sys.argv[1]
sums = calculate_moving_sums(get_hr_measurements(gpx_file), measured_window)

averages = [(x, round(s / measured_window)) for x, s in sums]

# your lactate threshold is average of last 20 in 30 minutes of tempo run
time_stamp, lactate_thr = max(averages, key=itemgetter(1))

print("Your lactate threshold is {} bpm.\n".format(lactate_thr))

time_and_hr = [ (get_time(trkpt), get_hr(trkpt)) for trkpt in get_trkpts(gpx_file) ]

if(plot_hr):
    pyplot.figure(1)
    pyplot.subplot(211)

    average_hr = [lactate_thr for _ in range(measured_window)]
    time_period = range(time_stamp, time_stamp + measured_window)
    pyplot.plot(time_period, average_hr)
    pyplot.plot([a for (_, a) in averages])
    pyplot.ylabel('HR bpm')
    pyplot.xlabel('second')

    pyplot.subplot(212)

    first_time_stamp = datetime.strptime(time_and_hr[0][0], '%Y-%m-%dT%H:%M:%SZ')

    hrs = []
    time_stamps = []

    for date_and_hr in time_and_hr:
        d1 = datetime.strptime(date_and_hr[0], '%Y-%m-%dT%H:%M:%SZ')
        diff = d1 - first_time_stamp;
        time_stamps.append(diff.total_seconds());
        hrs.append(date_and_hr[1])

    pyplot.plot(time_stamps, hrs)
    pyplot.show()
