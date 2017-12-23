try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'training_stats',
    'packages': ['training_stats'],
    'version': '0.1.0',
    'description': 'Training Stats',
    'author': 'Jakub Draganek',
    'author_email': 'jakub.draganek@gmail.com',
    'url': 'https://github.com/salwator/training_stats',
    'install_requires': ['numpy', 'geopy'],
    'scripts': [],
}

setup(**config)
