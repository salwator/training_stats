from unittest import TestCase

from .gpxfile import interpolate


class TestInterpolate(TestCase):
    def test_interpolate(self):
        points = [(1, 10), (2, 20), (5, 50)]
        expected = [(1, 10), (2, 20), (3, 30), (4, 40), (5, 50)]
        self.assertEqual(interpolate(points), expected)
