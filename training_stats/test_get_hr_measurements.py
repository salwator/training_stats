from unittest import TestCase

from .gpxfile import get_hr_measurements


class TestGet_hr_measurements(TestCase):
    def test_get_hr_measurements(self):
        hr = get_hr_measurements("./gpx/test_hr_short.gpx")
        self.assertEqual([(0, 73), (1, 73), (11, 82), (12, 90), (13, 96)], hr)
