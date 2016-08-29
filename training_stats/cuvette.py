#!/usr/bin/env python3

from gpxfile import get_trkpts, decode_iso_time, get_time, convert_time, interpolate
import sys
from geopy.distance import great_circle
import matplotlib.pyplot as pyplot

def get_time_intervals(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    time = [decode_iso_time(get_time(p, ns)) for p in trkpts]
    return [(time[i] - time[i-1]).total_seconds() for i in range(1, len(time))]


def get_elevation(trkpt, namespace):
    elevation_children = trkpt.find("./{0}ele".format(namespace))
    if elevation_children is not None:
        return elevation_children.text


def get_single_coordinates(trkpt):
    return (trkpt.attrib.get('lat'), trkpt.attrib.get('lon'))


def get_coordinates(trkpts): 
    return [(trkpt.attrib.get('lat'), trkpt.attrib.get('lon')) for trkpt in trkpts]


def get_distance(gpx_file):
    dists = get_distans_intervals(gpx_file)
    return [sum(dists[0:i]) for i in range(1, len(dists))]


def get_distans_intervals(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    points = get_coordinates(trkpts)
    return [great_circle((points[i-1][0], points[i-1][1]), (points[i][0], points[i][1])).miles * 1.609 for i in range(1, len(points))]


def get_elevation_in_time_measurements(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    data = [(get_time(p, ns), get_elevation(p, ns)) for p in trkpts]
    start_time = decode_iso_time(data[0][0])
    return [(convert_time(t, start_time), elev) for (t, elev) in data if elev]


def get_elevation_in_distans_measurements(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    distance = get_distance(gpx_file)
    return [(distance[p]*1000, get_elevation(trkpts[p], ns)) for p in range(0, len(trkpts)-2)]


def get_pace_measurements(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    distance = get_distance(gpx_file)
    distans_intervals = get_distans_intervals(gpx_file)
    time = [get_time(p, ns) for p in trkpts]
    time_intervals = get_time_intervals(gpx_file)
    pace = [(convert_time(time[p], decode_iso_time(time[0])), ((time_intervals[p]/60) / distans_intervals[p])) for p in range(len(distance)) if distans_intervals[p] != 0]  # pace in min/km
    return pace


def main():
    gpx_file = sys.argv[1] 
    print("Loading gpx: {}".format(gpx_file))

    elevations_in_time = interpolate(get_elevation_in_time_measurements(gpx_file))
    elevations_in_distans = interpolate(get_elevation_in_distans_measurements(gpx_file))
    pace_in_time = interpolate(get_pace_measurements(gpx_file))

    time, elev = zip(*elevations_in_time)

    pyplot.subplot(311)
    pyplot.plot(time, elev, 'b') 
    pyplot.xlabel('Time [s]')
    pyplot.ylabel('Elevation')

    dist, elev = zip(*elevations_in_distans)

    pyplot.subplot(312)
    pyplot.plot(dist, elev, 'b') 
    pyplot.xlabel('Distans [m]')
    pyplot.ylabel('Elevation')

    time2, pace = zip(*pace_in_time)

    pyplot.subplot(313)
    pyplot.plot(time2, pace, 'b') 
    pyplot.xlabel('Time [s]')
    pyplot.ylabel('Pace [min/km]')

    pyplot.show()


if __name__ == "__main__":
    main()
