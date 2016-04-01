#!/usr/bin/env python3


from xml.dom.minidom import parse
from operator import itemgetter
import matplotlib.pyplot as pyplot
from datetime import timedelta, datetime
from scipy.interpolate import UnivariateSpline
import sys

# assume sampling time is 1s
measured_window = 60 * 20

# set off to disable plotting
plot_hr = True

def get_trkpts(gpx_file):
    gpx = parse(gpx_file)
    return gpx.childNodes[0].getElementsByTagName("trkpt")

def get_time(trkpt):
    time_children = trkpt.getElementsByTagName("time") 
    if time_children:
        return time_children[0].childNodes[0].toxml()

def get_hr(trkpt):
    hr_children =trkpt.getElementsByTagName('gpxtpx:hr')
    if hr_children:
        return int(hr_children[0].childNodes[0].wholeText)

def convert_time(time, start):
    t = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    dt = t - start
    return dt.total_seconds()

def get_hr_measurements(gpx_file):
    points = get_trkpts(gpx_file) 
    data = [ (get_time(p), get_hr(p)) for p in points ]
    start_time = datetime.strptime(data[0][0], '%Y-%m-%dT%H:%M:%SZ')
    return [ (convert_time(t, start_time), hr) for (t, hr) in data if hr ]

def interpolate(points):
    split = list(zip(*points))
    spl = UnivariateSpline(split[0],split[1])
    time_stamps = list(range(int(split[0][-1])))
    new_hrs = spl(time_stamps)
    return list(zip(time_stamps, new_hrs))

def calculate_moving_sums(measures, windowlen):
    limit = len(measures) - windowlen
    hrs =  [ hr for _, hr in measures ]
    return [(time_point, sum(hrs[time_point:time_point+windowlen]))
            for time_point in range(0, limit)]

gpx_file = sys.argv[1]
print("Loading gpx: {}".format(gpx_file))

hrs = get_hr_measurements(gpx_file)
sums = calculate_moving_sums(interpolate(hrs) , measured_window)

averages = [(x, round(s / measured_window)) for x, s in sums]

# your lactate threshold is average of last 20 in 30 minutes of tempo run
time_stamp, lactate_thr = max(averages, key=itemgetter(1))

print("Your lactate threshold is {} bpm.\n".format(lactate_thr))

time_and_hr = [ (get_time(trkpt), get_hr(trkpt)) for trkpt in get_trkpts(gpx_file) ]

if(plot_hr):
    pyplot.figure(1)
    pyplot.subplot(311)

    average_hr = [lactate_thr for _ in range(measured_window)]
    time_period = range(time_stamp, time_stamp + measured_window)
    pyplot.plot(time_period, average_hr)
    pyplot.plot([a for (_, a) in averages])
    pyplot.ylabel('HR bpm')
    pyplot.xlabel('second')

    pyplot.subplot(312)

    first_time_stamp = datetime.strptime(time_and_hr[0][0], '%Y-%m-%dT%H:%M:%SZ')

    hrs_z = []
    time_stamps = []

    for date_and_hr in time_and_hr:
        d1 = datetime.strptime(date_and_hr[0], '%Y-%m-%dT%H:%M:%SZ')
        diff = d1 - first_time_stamp;
        time_stamps.append(diff.total_seconds());
        hrs_z.append(date_and_hr[1])

    pyplot.plot(time_stamps, hrs_z)

    pyplot.subplot(313)

    interpolate_hrs = list(zip(*interpolate(hrs)))
   
    pyplot.plot(interpolate_hrs[0], interpolate_hrs[1])

    pyplot.show()
