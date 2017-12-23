# Training Statistics [![Build Status](https://travis-ci.org/salwator/training_stats.svg?branch=master)](https://travis-ci.org/salwator/training_stats) [![Maintainability](https://api.codeclimate.com/v1/badges/0f1bf97059152dabb9c8/maintainability)](https://codeclimate.com/github/salwator/training_stats/maintainability)
My aim in this project is to develop set of useful scripts for analyzing data collected by modern running/cycling watches.

## Installation

To use _training_stats_ library in your project you will need Python in version 3.4 or newer.
Run `pip install training_stats` to install package.


## Examples

To run examples clone repository.

```bash
# git clone https://github.com/salwator/training_stats.git
# cd training_stats
```

In `examples` directory you can find some playground using library. To use those scripts you will need requirements installed. You might want to use virtualenv to not polute your system environment.

```bash
# pip install -r requirements.txt
```

Then `# cd examples` and play :smile:

## Available tools

Since project is in early phase only one script is in useful state.
With [half hour test](training_stats/half_hour_test.py) script you can calculate result of 30 minute endurance test.
Result is lactate threshold, which is great for determining your heart rate zones. You can calculate your zones [here](http://www.datacranker.com/heart-rate-zones/).

