import heapq
from elf import Elf
from hours import Hours
import math
import datetime

__author__ = 'ktao'


class BusyElvesHeap:
    def __init__(self, num_elves):
        self.elf_heap = []
        self.hours = Hours()
        self.ref_time = datetime.datetime(2014, 1, 1, 0, 0)
        for i in range(1, num_elves + 1):
            elf = Elf(i)
            heapq.heappush(self.elf_heap, (elf.next_available_time, elf))

    def get_elves_for_min(self, elf_available_time):
        elves_for_min = []

        while len(self.elf_heap) > 0 and self.elf_heap[0][1].next_available_time <= elf_available_time:
            available_time, elf = heapq.heappop(self.elf_heap)
            elves_for_min.append(elf)
        return elves_for_min

    def assign_toy_to_elf(self, elf, toy, work_start_time, solution_writer):
        """
        :param elf:
        :param toy:
        :param work_start_time:
        :return: a string representing the row
        """
        elf.next_available_time, work_duration = self.calculate_next_available_and_duration(work_start_time, elf, toy,
                                                                                            self.hours)
        elf.update_elf(self.hours, toy, work_start_time, work_duration)
        heapq.heappush(self.elf_heap, (elf.next_available_time, elf))

        solution_writer.write(toy, elf, work_start_time, work_duration)

    @staticmethod
    def calculate_next_available_and_duration(input_time, current_elf, current_toy, hrs):
        """ Given a toy, assigns the next elf to the toy. Computes the elf's updated rating,
        applies the rest period (if any), and sets the next available time.
        :param input_time: list of tuples (next_available_time, elf)
        :param current_elf: elf object
        :param current_toy: toy object
        :param hrs: hours object
        :return: list of elves in order of next available
        """
        start_time = hrs.next_sanctioned_minute(
            input_time)  # double checks that work starts during sanctioned work hours
        duration = int(math.ceil(current_toy.duration / current_elf.rating))
        sanctioned, unsanctioned = hrs.get_sanctioned_breakdown(start_time, duration)

        if unsanctioned == 0:
            return hrs.next_sanctioned_minute(start_time + duration), duration
        else:
            return hrs.apply_resting_period(start_time + duration, unsanctioned), duration