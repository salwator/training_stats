#!/usr/bin/env python3

from half_hour_test import get_trkpts, decode_iso_time, get_time, convert_time, interpolate
import sys
from geopy.distance import great_circle

def get_time_intervals(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    time = [decode_iso_time(get_time(p, ns)) for p in trkpts]
    return [(time[i] - time[i-1]).total_seconds() for i in range(1, len(time))]


def get_elevation(trkpt, namespace):
    elevation_children = trkpt.find("./{0}ele".format(namespace))
    if elevation_children is not None:
        return elevation_children.text


def get_points(trkpts): 
    return [(trkpt.attrib.get('lat'), trkpt.attrib.get('lon')) for trkpt in trkpts]


def get_distans(gpx_file):
    dists = get_distans_intervals(gpx_file)
    return [sum(dists[0:i]) for i in range(1, len(dists))]


def get_distans_intervals(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    points = get_points(trkpts)
    return [great_circle((points[i-1][0], points[i-1][1]), (points[i][0], points[i][1])).miles * 1.609 for i in range(1, len(points))]


def get_elevation_measurements(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    data = [(get_time(p, ns), get_elevation(p, ns)) for p in trkpts]
    start_time = decode_iso_time(data[0][0])
    return [(convert_time(t, start_time), elev) for (t, elev) in data if elev]


def main():
    gpx_file = sys.argv[1] 
    print("Loading gpx: {}".format(gpx_file)) 

if __name__ == "__main__":
    main()
