from xml.dom.minidom import parse
from operator import itemgetter
import sys
import matplotlib.pyplot as plt

def getHrsFromGpx(gpx_file):
    gpx = parse(gpx_file)
    return [ int(hr.childNodes[0].wholeText) for hr in gpx.getElementsByTagName('gpxtpx:hr') ]

gpx_file = sys.argv[1]
hrs = getHrsFromGpx(gpx_file)

# assume sampling time is 1s
num_of_hr = 60 * 20

limit = len(hrs) - num_of_hr

print("Checking for {} in {}\n".format(num_of_hr, limit))

sums = [ (x, sum(hrs[x:x+num_of_hr])) for x in range(0,limit) ]
averages = [ (x, round(s / num_of_hr)) for x, s in sums ]

# your lactate threshold is average of alst 20 minutes in 30 minutes of tempo run
lactate_thr = max(averages, key=itemgetter(1))

print("Your lactate threshold is {} measured between {} and {} second.\n"
      .format(lactate_thr[1],
              lactate_thr[0],
              lactate_thr[0]+num_of_hr))

plt.plot( [a for _,a in averages] )
plt.ylabel('HR bpm')
plt.xlabel('second')
plt.show()
