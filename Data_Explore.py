import os
import csv
import time
import math
import datetime

import matplotlib

from hours import Hours
from toy import Toy
from elf import Elf


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

    for i in xrange(1, NUM_TOYS+1):
        myToy = myToys[str(i)]
        if myToy.duration >= 600:
            toy_greater_than_600_count+=1
        if myToy.duration >= 2400:
            toy_greater_than_2400_count+=1
        if myToy.duration > max_toy_duration:
            max_toy_duration = myToy.duration

    print('num toys greater than 600 : ' + str(toy_greater_than_600_count))
    print('num toys greater than 2400 : ' + str(toy_greater_than_2400_count))
    print('max duration : ' + str(max_toy_duration))
    print('total time = {0}'.format(time.time() - start))