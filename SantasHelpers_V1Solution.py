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

def solution(toy_file, soln_file):
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
    busy_elves_heap = BusyElvesHeap(900)
    toy_backlog = ToyBacklog()
    elves_ready = ElvesReady()
    scheduler = Scheduler()

    current_time = 540

    while not (toy_loader.done() and toy_backlog.done()):
        if (toy_loader.done() and len(toy_backlog.easy_toy_list) == 0):
            # clean up last toys
            print("cleaning up final toys")


        # step 1 process newly arrived toys and fresh elves
        new_toy_orders = toy_loader.get_toys_up_to_minute(current_time)
        new_elves = busy_elves_heap.get_elves_for_min(current_time)

        toy_backlog.add_toys_to_backlog(new_toy_orders)
        elves_ready.add_elves(new_elves)

        # step 2 pair off as many elves and toys as possible

        scheduler.schedule(toy_backlog, elves_ready, busy_elves_heap, current_time, solution_writer)

        current_time = hrs.next_sanctioned_minute(current_time)



    toy_loader.close()
    solution_writer.close()



# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    print ('starting Naive Solution')

    start = time.time()

    NUM_ELVES = 900

    toy_file = os.path.join(os.getcwd(), '75ktoys.csv')
    soln_file = os.path.join(os.getcwd(), 'test_sub.csv')

    solution(toy_file, soln_file)

    print ('total runtime = {0}'.format(time.time() - start))
