from ..training_stats.gpxfile import get_hr_measurements


def test_get_hr_measurements():
    hr = get_hr_measurements("./gpx/test_hr_short.gpx")
    assert hr == [(0, 73), (1, 73), (11, 82), (12, 90), (13, 96)]
