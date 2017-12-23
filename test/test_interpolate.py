from training_stats.gpxfile import interpolate


def test_interpolate():
    points = [(1, 10), (2, 20), (5, 50)]
    expected = [(1, 10), (2, 20), (3, 30), (4, 40), (5, 50)]
    assert interpolate(points) == expected
