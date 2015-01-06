""" This solution uses Joyce Noah-Vanhoucke's naive solution as a template, but adds some different approaches.
 This is my first time programming in python so this is also to help me learn it.

  Algorithm in pseudo-code:

  1. Each day load in all of the toys that will arrive that day, or have arrived before.
  2. Split the toys into toys that can be finished today, and toys that cannot possibly be finished today.
        Put the ones that cannot be finished today into a "todo" list for later.
  3. Optimize it so the the most number of elves have the most full day possible.

  this pattern should work well for all toys that take less than one full day (40 elf-hours (or 2400 elf-minutes)) for a 4.0 rated elf.

  There's about 2 million toys that take more than 2400 elf-minutes. About 8 million toys that take less than 2400 elf-minutes.

  """
from busy_elves_heap import BusyElvesHeap
from elves_ready import ElvesReady
from scheduler import Scheduler
from solution_writer import SolutionWriter
from toy_backlog import ToyBacklog
from toy_loader import ToyLoader

__author__ = 'Kevin Tao'
__date__ = 'December 17, 2014'

import os
import csv
import math
import heapq
import time
import datetime

from hours import Hours
from toy import Toy
from elf import Elf

# ========================================================================== #

def solution(toy_file, soln_file, num_elves, TARGET):
    """ Creates a simple solution where the next available elf is assigned a toy. Elves do not start
    work outside of sanctioned hours.
    :param toy_file: filename for toys file (input)
    :param soln_file: filename for solution file (output)
    :param myelves: list of elves in a priority queue ordered by next available time
    :return:
    """
    hrs = Hours()

    toy_loader = ToyLoader(toy_file)
    solution_writer = SolutionWriter(soln_file)
    busy_elves_heap = BusyElvesHeap(num_elves)

    elves_ready = ElvesReady()
    scheduler = Scheduler(TARGET)

    start = time.time()

    current_time = 482940

    print("Getting initial toys")
    print('time taken = {0}, current_time = {1}'.format(time.time() - start, hrs.get_time_string(current_time)))
    new_toy_orders = toy_loader.get_toys_up_to_minute(current_time)

    print("Loading initial toys into backlog")
    print('time taken = {0}, current_time = {1}'.format(time.time() - start, hrs.get_time_string(current_time)))
    toy_backlog = ToyBacklog(new_toy_orders)

    print("Finished initializing toys into backlog")
    print('time taken = {0}, current_time = {1}'.format(time.time() - start, hrs.get_time_string(current_time)))

    toys_finished = 0

    toys_left_at_end = []

    time_of_last_toy_assigned = 0

    while not (toy_loader.done() and toy_backlog.done() and len(toys_left_at_end) == 0):

        # step 1 process newly arrived toys and fresh elves
        new_toy_orders = toy_loader.get_toys_up_to_minute(current_time)
        new_elves = busy_elves_heap.get_elves_for_min(current_time)

        toy_backlog.add_toys_to_backlog(new_toy_orders)
        elves_ready.add_elves(new_elves)

        if (current_time % 120 == 60):
            print('time taken = {0}, current_time = {1}'.format(time.time() - start, hrs.get_time_string(current_time)))
            print('easy_toys:{0},\t constant_toys:{1},\t variable_toys:{2},\t hardest_toys:{3},\t toys_left_at_end:{4}'.format(
                len(toy_backlog.easy_toy_list), len(toy_backlog.constant_rating_list),
                len(toy_backlog.variable_toy_list), len(toy_backlog.hardest_toy_list), len(toys_left_at_end)))
            print('elves ready:{0}, high-perf-elves:{1}'.format(len(elves_ready.training_elf_list),
                                                                len(elves_ready.high_performance_elf_list)))
            print('toys finished = {0}'.format(toys_finished))

        if (toy_loader.done() and current_time - time_of_last_toy_assigned > 1440 and len(elves_ready.training_elf_list) == num_elves and len(toys_left_at_end) == 0):
            print("starting cleanup")
            for toy in toy_backlog.easy_toy_list:
                toys_left_at_end.append(toy)
            toy_backlog.easy_toy_list.clear()
            for toy in toy_backlog.constant_rating_list:
                toys_left_at_end.append(toy)
            toy_backlog.constant_rating_list = []
            while len(toy_backlog.variable_toy_list) > 0:
                toys_left_at_end.append(toy_backlog.pop_variable_toy())
            while len(toy_backlog.hardest_toy_list) > 0:
                toys_left_at_end.append(toy_backlog.pop_hardest_toy())

        if (toy_loader.done() and len(toys_left_at_end) > 0):
            # clean up last toys
            toys_finished += scheduler.clean_up(toys_left_at_end, elves_ready, busy_elves_heap, current_time, solution_writer)

        else:
            # step 2 pair off as many elves and toys as possible
            toys_newly_finished = scheduler.schedule(toy_backlog, elves_ready, busy_elves_heap, current_time,
                                                solution_writer, toy_loader)
            toys_finished += toys_newly_finished
            if (toys_newly_finished > 0):
                time_of_last_toy_assigned = current_time

        current_time = hrs.next_sanctioned_minute(current_time)

    toy_loader.close()
    solution_writer.close()


# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    start = time.time()

    NUM_ELVES = 800

    TARGET = 0.5

    print('starting V1 Solution submission target ' + str(TARGET) + '  ' + str(NUM_ELVES) + ' elves ' + str(start) + '.csv')

    toy_file = os.path.join(os.getcwd(), 'toys_rev2.csv')
    soln_file = os.path.join(os.getcwd(), 'submission target ' + str(TARGET) + '  ' + str(NUM_ELVES) + ' elves ' + str(start) + '.csv')

    solution(toy_file, soln_file, NUM_ELVES, TARGET)

    print('total runtime = {0}'.format(time.time() - start))
