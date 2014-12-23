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

def create_elves(NUM_ELVES):
    """ Elves are stored in a sorted list using heapq to maintain their order by next available time.
    List elements are a tuple of (next_available_time, elf object)
    :return: list of elves
    """
    list_elves = []
    for i in range(1, NUM_ELVES+1):
        elf = Elf(i)
        heapq.heappush(list_elves, (elf.next_available_time, elf))
    return list_elves


def assign_elf_to_toy(input_time, current_elf, current_toy, hrs):
    """ Given a toy, assigns the next elf to the toy. Computes the elf's updated rating,
    applies the rest period (if any), and sets the next available time.
    :param input_time: list of tuples (next_available_time, elf)
    :param current_elf: elf object
    :param current_toy: toy object
    :param hrs: hours object
    :return: list of elves in order of next available
    """
    start_time = hrs.next_sanctioned_minute(input_time)  # double checks that work starts during sanctioned work hours
    duration = int(math.ceil(current_toy.duration / current_elf.rating))
    sanctioned, unsanctioned = hrs.get_sanctioned_breakdown(start_time, duration)

    if unsanctioned == 0:
        return hrs.next_sanctioned_minute(start_time + duration), duration
    else:
        return hrs.apply_resting_period(start_time + duration, unsanctioned), duration





def solution_firstAvailableElf(toy_file, soln_file, myelves):
    """ Creates a simple solution where the next available elf is assigned a toy. Elves do not start
    work outside of sanctioned hours.
    :param toy_file: filename for toys file (input)
    :param soln_file: filename for solution file (output)
    :param myelves: list of elves in a priority queue ordered by next available time
    :return:
    """
    hrs = Hours()
    ref_time = datetime.datetime(2014, 1, 1, 0, 0)
    row_count = 0
    with open(toy_file) as f:
        toysfile = csv.reader(f)
        next(toysfile)  # header row

        with open(soln_file, 'wt') as w:
            wcsv = csv.writer(w)
            wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

            for row in toysfile:
                current_toy = Toy(row[0], row[1], row[2])

                # get next available elf
                elf_available_time, current_elf = heapq.heappop(myelves)

                work_start_time = elf_available_time
                if current_toy.arrival_minute > elf_available_time:
                    work_start_time = current_toy.arrival_minute

                # work_start_time cannot be before toy's arrival
                if work_start_time < current_toy.arrival_minute:
                    print ('Work_start_time before arrival minute: {0}, {1}'.\
                        format(work_start_time, current_toy.arrival_minute))
                    exit(-1)

                current_elf.next_available_time, work_duration = \
                    assign_elf_to_toy(work_start_time, current_elf, current_toy, hrs)
                current_elf.update_elf(hrs, current_toy, work_start_time, work_duration)

                # put elf back in heap
                heapq.heappush(myelves, (current_elf.next_available_time, current_elf))

                # write to file in correct format
                tt = ref_time + datetime.timedelta(seconds=60*work_start_time)
                time_string = " ".join([str(tt.year), str(tt.month), str(tt.day), str(tt.hour), str(tt.minute)])
                wcsv.writerow([current_toy.id, current_elf.id, time_string, work_duration])


# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    print ('starting Naive Solution')

    start = time.time()

    NUM_ELVES = 900

    toy_file = os.path.join(os.getcwd(), 'toys_rev2.csv')
    soln_file = os.path.join(os.getcwd(), 'sampleSubmission_rev2.csv')

    myelves = create_elves(NUM_ELVES)
    solution_firstAvailableElf(toy_file, soln_file, myelves)

    print ('total runtime = {0}'.format(time.time() - start))
