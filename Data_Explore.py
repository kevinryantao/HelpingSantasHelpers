import os
import csv
import time
import math
import datetime

from numpy import *
import matplotlib.pyplot as plt
import pandas as pd

from hours import Hours
from toy import Toy
from elf import Elf

"""

    Summary of what I discovered from data exploration:

    The histogram of toys follows : # of toys ~ 1 / duration of toy

    Thus the total amount of time spent building each duration-bin of toys is essentially constant.

    The total amount of time spent on building each duration-bin of 60 minutes is ~ 20 million minutes.

    The range is from 0 to 22500, with a maybe only a dozen between 22500 and 30000.

"""


def read_toys(toy_file, num_toys):
    """ Reads the toy file and returns a dictionary of Toys.
    Toy file format: ToyId, Arrival_time, Duration
        ToyId: toy id
        Arrival_time: time toy arrives. Format is: YYYY MM DD HH MM (space-separated)
        Duration: duration in minutes to build toy
    :param toy_file: toys input file
    :param hrs: hours object
    :param num_toys: total number of toys to build
    :return: Dictionary of toys
    """
    toy_dict = {}
    with open(toy_file) as f:
        fcsv = csv.reader(f)
        next(fcsv)  # header row
        for row in fcsv:
            new_toy = Toy(row[0], row[1], row[2])
            toy_dict[new_toy.id] = new_toy
    if len(toy_dict) != num_toys:
        print('\n ** Read a file with {0} toys, expected {1} toys. Exiting.'.format(len(toy_dict), num_toys))
        exit(-1)
    return toy_dict


if __name__ == '__main__':

    """
    x = arange(0.,10.,0.1) # generate a range of values as an array, using begin, end, step as input
    y = arange(0.,10.,0.1)
    ll = plt.plot(x,y) # this is the simplest plotting idiom
    plt.show()

    print('End program')

    """

    toys = pd.read_csv('toys_rev2.csv')
    duration = toys['Duration']
    #p = duration.hist(bins=1000)
    """
    bins1=arange(0,2400,60)
    bins2=arange(2400,30000,600)

    binslist = list(bins1)
    for i in bins2:
        binslist.append(i)
    """
    binslist=arange(0, 30000, 60)
    fullArray = binslist

    values, bins, others = plt.hist(duration, bins=fullArray, log=True)
    totalJobTime = ndarray(values.size)
    totalJobTimeXAxis = ndarray(values.size)
    for i in range(0, bins.size - 1, 1):
        totalJobTime[i] = values[i] * (bins[i] + bins[i+1]) / 2.
        totalJobTimeXAxis[i] = (bins[i] + bins[i+1]) / 2.



    plt.plot(totalJobTimeXAxis, totalJobTime)
    plt.show()

    print('End plotting')

    print('Beginning data exploration')

    start = time.time()

    NUM_TOYS = 10000000
    NUM_ELVES = 900

    toy_file = os.path.join(os.getcwd(), 'toys_rev2.csv')
    myToys = read_toys(toy_file, NUM_TOYS)

    current_time = time.time()

    print('Finished reading all toys.')
    print('total time = {0}'.format(time.time() - start))

    toy_greater_than_600_count = 0
    toy_greater_than_2400_count = 0
    max_toy_duration = 0

    for i in range(1, NUM_TOYS+1):
        myToy = myToys[str(i)]
        if myToy.duration >= 600:
            toy_greater_than_600_count += 1
        if myToy.duration >= 2400:
            toy_greater_than_2400_count += 1
        if myToy.duration > max_toy_duration:
            max_toy_duration = myToy.duration

    print('num toys greater than 600 : ' + str(toy_greater_than_600_count))
    print('num toys greater than 2400 : ' + str(toy_greater_than_2400_count))
    print('max duration : ' + str(max_toy_duration))
    print('total time = {0}'.format(time.time() - start))