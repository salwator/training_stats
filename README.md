# Training Statistics   ![travis](https://travis-ci.org/salwator/training_stats.svg?branch=master)

My aim in this project is to develop set of useful scripts for analyzing data collected by modern running/cycling watches.

## Installation

You will need Python in version 3.4 or newer.
Run `make` to install dependencies in local virtualenv.

If you want to install dependencies system-wide you can use `sudo pip install -r requirements.txt`.

## Available tools

Since project is in early phase only one script is in useful state.
With [half hour test](training_stats/half_hour_test.py) script you can calculate result of 30 minute endurance test.
Result is lactate threshold, which is great for determining your heart rate zones. You can calculate your zones [here](http://www.datacranker.com/heart-rate-zones/).

