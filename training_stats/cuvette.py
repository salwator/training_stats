#!/usr/bin/env python3

import half_hour_test
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


def get_total_distans_in_km(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    points = get_points(trkpts)
    sum_of_dist = 0
    dists = []
    for i in range(len(points)-1):
        first_point = (points[i][0], points[i][1])
        second_point = (points[i+1][0], points[i+1][1])
        dist = great_circle(first_point, second_point).miles
        sum_of_dist += dist
        #print("Added dist in m: ", sum_of_dist * 1.609);
        dists.append(sum_of_dist * 1.609)
    dists.append(sum_of_dist * 1.609)
    #print("Distans in m: ", sum_of_dist * 1.609)
    #print("Dist len: ", len(dists))
    #print("Time len: ", len(trkpts))
    return dists


def get_distans_intervals(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    points = get_points(trkpts)
    sum_of_dist = 0
    dists = []
    for i in range(len(points)-1):
        first_point = (points[i][0], points[i][1])
        second_point = (points[i+1][0], points[i+1][1])
        dist = great_circle(first_point, second_point).miles
        #sum_of_dist += dist
        #print("Added dist in m: ", sum_of_dist * 1.609);
        dists.append(dist * 1.609)
    dists.append(dist * 1.609)
    #print("Distans in m: ", sum_of_dist * 1.609)
    #print("Dist len: ", len(dists))
    #print("Time len: ", len(trkpts))
    return dists


def get_elevation_measurements(gpx_file):
    ns, trkpts = get_trkpts(gpx_file)
    data = [(get_time(p, ns), get_elevation(p, ns)) for p in trkpts]
    start_time = decode_iso_time(data[0][0])
    return [(convert_time(t, start_time), elev) for (t, elev) in data if elev]


def main():
    time_intervals = get_time_intervals(gpx_file)
    dists = get_total_distans_in_km(gpx_file)
    dists_list = get_distans_intervals(gpx_file)
    t2, elev2 = zip(*get_elevation_measurements(gpx_file))

    plot_elevation = False

    # elevation in time
    elevations = interpolate(get_elevation_measurements(gpx_file))
    measured_elevation_time, measured_elevations = zip(*elevations[start_measure:stop_measure])


    if(plot_elevation):
        t, elev = zip(*elevations)
        pyplot.subplot(412)
        pyplot.plot(t, elev, 'g')
        pyplot.plot(measured_elevation_time, measured_elevations, 'r')
        pyplot.xlabel('Time [s]')
        pyplot.ylabel('Elevation')

        pyplot.subplot(413)
        pyplot.plot(dists, elev2, 'g')
        pyplot.xlabel('Distans [m]')
        pyplot.ylabel('Elevation')

        pace_intervals = [(time_intervals[i]/60)/(dists_list[i]) for i in range(len(time_intervals) - 1)]
        time_sum = [(time_intervals[i] + time_intervals[i-1]) for i in range(1, len(time_intervals))]
        time_sum = [sum(time_intervals[0:i]) for i in range(1, len(time_intervals))]
        
        #print pace_intervals
        #print time_intervals
        #print time_sum

        pyplot.subplot(414)
        pyplot.plot(time_sum, pace_intervals, 'b')
        pyplot.xlabel('Time [s]')
        pyplot.ylabel('Pace [min/km]')
