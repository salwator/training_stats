import re
import xml.etree.cElementTree as ET
from datetime import datetime



def get_time(trkpt, namespace):
    time_children = trkpt.find("./{0}time".format(namespace))
    if time_children is not None:
        return time_children.text


def get_hr(trkpt, namespace):
    extension_children = trkpt.find('./{0}extensions/./'.format(namespace))
    if extension_children is not None:
        ext_ns = re.match('\{.*\}', extension_children.tag).group(0)
        hr_child = extension_children.find('./{0}hr'.format(ext_ns))
        if hr_child is not None:
            return int(hr_child.text)


def decode_iso_time(timestr):
    return datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%SZ")


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
