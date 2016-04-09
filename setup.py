try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Training Stats',
    'author': 'Jakub Draganek',
    'author_email': 'jakub.draganek@gmail.com',
    'version': '0.1',
    'install_requires': ['flask', 'nose', 'numpy', 'matplotlib', 'geopy'],
    'packages': ['training_stats'],
    'scripts': [],
    'name': 'training_stats'
}

setup(**config)
