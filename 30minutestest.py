from xml.dom.minidom import parse
from operator import itemgetter
import matplotlib.pyplot as pyplot

import datetime
import sys

# assume sampling time is 1s
measured_window = 60 * 20

# set off to disable plotting
plot_hr = True


def get_hr_measurements(gpx_file):
    gpx = parse(gpx_file)
    return [ int(hr.childNodes[0].wholeText) for hr in gpx.getElementsByTagName('gpxtpx:hr') ]

def calculate_moving_sums(measures, windowlen):
    limit = len(measures) - windowlen
    return [ (time_point, sum(measures[time_point:time_point+windowlen]))
             for time_point in range(0,limit) ]


gpx_file = sys.argv[1]
sums = calculate_moving_sums(get_hr_measurements(gpx_file), measured_window)

averages = [ (x, round(s / measured_window)) for x, s in sums ]

# your lactate threshold is average of alst 20 minutes in 30 minutes of tempo run
time_stamp,lactate_thr = max(averages, key=itemgetter(1))

print("Your lactate threshold is {} bpm.\n".format(lactate_thr))

if(plot_hr):
    average_hr = [ lactate_thr for _ in range(measured_window) ]
    time_period = range(time_stamp, time_stamp + measured_window)
    pyplot.plot(time_period, average_hr)
    pyplot.plot( [a for _,a in averages] )
    pyplot.ylabel('HR bpm')
    pyplot.xlabel('second')
    pyplot.show()
