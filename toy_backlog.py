import heapq

__author__ = 'ktao'
import datetime
import math
import bisect
from sorted_collection import SortedCollection
from operator import attrgetter, methodcaller
from hours import Hours


class ToyBacklog:
    def __init__(self, initial_toys):
        self.rating_threshold = 3.95
        self.easy_toy_duration_threshold = 10 * 60 * self.rating_threshold
        self.constant_rating_list = []
        self.constant_rating_threshold = 12 * 60 * 4
        self.variable_toy_list = []
        self.variable_rating_threshold = 61.955 * 60 * 4
        self.hardest_toy_list = []
        easy_toy_temp_list = []
        for toy in initial_toys:
            if toy.duration < self.easy_toy_duration_threshold:
                easy_toy_temp_list.append(toy)
            elif self.easy_toy_duration_threshold <= toy.duration <= self.constant_rating_threshold:
                self.constant_rating_list.append(toy)
            elif toy.duration <= self.variable_rating_threshold:
                self.variable_toy_list.append((-1 * toy.penalty_assuming_4elf_and_max_sanctioned(), toy))
            else:
                self.hardest_toy_list.append((-1 * toy.duration, toy))
        self.easy_toy_list = SortedCollection(iterable=easy_toy_temp_list, key=attrgetter('duration'))
        heapq.heapify(self.variable_toy_list)
        heapq.heapify(self.hardest_toy_list)

    def get_best_fit_easy_toy(self, max_toy_duration):
        try:
            ret = self.easy_toy_list.find_le(max_toy_duration)
        except ValueError:
            ret = None
        return ret

    def add_toy_to_backlog(self, toy):
        if toy.duration < self.easy_toy_duration_threshold:
            self.easy_toy_list.insert(toy)
        elif self.easy_toy_duration_threshold <= toy.duration <= self.constant_rating_threshold:
            self.constant_rating_list.append(toy)
        elif toy.duration <= self.variable_rating_threshold:
            heapq.heappush(self.variable_toy_list, (-1 * toy.penalty_assuming_4elf_and_max_sanctioned(), toy))
        else:
            heapq.heappush(self.hardest_toy_list, (-1 * toy.duration, toy))

    def add_toys_to_backlog(self, toys):
        for toy in toys:
            self.add_toy_to_backlog(toy)

    def pop_variable_toy(self):
        return heapq.heappop(self.variable_toy_list)[1]

    def pop_hardest_toy(self):
        return heapq.heappop(self.hardest_toy_list)[1]

    def done(self):
        return len(self.easy_toy_list) == 0 and len(self.constant_rating_list) == 0 and len(
            self.variable_toy_list) == 0 and len(self.hardest_toy_list) == 0