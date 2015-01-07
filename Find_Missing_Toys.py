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



def remove_built_toys(myToys, submission_file):
    myMissingToys = myToys.copy()
    with open(submission_file) as f:
        fcsv = csv.reader(f)
        next(fcsv)  # header row
        for row in fcsv:
            toyId = row[0]
            myMissingToys.pop(toyId, None)
    return myMissingToys


if __name__ == '__main__':

    print('Beginning data exploration')

    start = time.time()

    NUM_TOYS = 10000000
    NUM_ELVES = 900

    toy_file = os.path.join(os.getcwd(), 'toys_rev2.csv')
    myToys = read_toys(toy_file, NUM_TOYS)

    current_time = time.time()

    print('Finished reading all toys.')
    print('total time = {0}'.format(time.time() - start))

    submission_file = os.path.join(os.getcwd(), 'v3 submission target 0.5  900 elves 1420653828.63084.csv')

    myMissingToys = remove_built_toys(myToys, submission_file)


    print('Finished removing all built toys.')
    print('total time = {0}'.format(time.time() - start))


    myDurations = []

    for key in myMissingToys:
        myDurations.append(myMissingToys[key].duration)

    binslist=arange(0, 30000, 60)
    fullArray = binslist

    values, bins, others = plt.hist(myDurations, bins=fullArray, log=True)
    totalJobTime = ndarray(values.size)
    totalJobTimeXAxis = ndarray(values.size)
    for i in range(0, bins.size - 1, 1):
        totalJobTime[i] = values[i] * (bins[i] + bins[i+1]) / 2.
        totalJobTimeXAxis[i] = (bins[i] + bins[i+1]) / 2.



    plt.plot(totalJobTimeXAxis, totalJobTime)
    plt.show()

    print('End plotting')
