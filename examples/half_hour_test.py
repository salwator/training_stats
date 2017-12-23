import sys
import matplotlib.pyplot as pyplot
from ..training_stats.gpsfile import get_hr_measurements
from ..training_stats.hrm import calculate_lactate_threshold


def main():
    ''' Run with GPX file as first argument '''
    plot_hr = False  # turn off to disable data plotting

    gpx_file = sys.argv[1]
    print("Loading gpx: {}".format(gpx_file))

    hrdata = get_hr_measurements(gpx_file)
    lactate_thr, measured_time, measured_hrs = calculate_lactate_threshold(hrdata)

    print("Your lactate threshold is {} bpm.".format(lactate_thr))
    if(plot_hr):
        print('Plotting training data')
        t, hr = zip(*hrdata)
        pyplot.plot(t, hr, 'b')
        pyplot.plot(measured_time, measured_hrs, 'r')
        pyplot.xlabel('Time [s]')
        pyplot.ylabel('Hart rate [bpm]')
        pyplot.show()


if __name__ == "__main__":
    main()
