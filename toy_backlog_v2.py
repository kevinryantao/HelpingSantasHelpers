import heapq
from easy_toy_backlog import EasyToyBacklog

__author__ = 'ktao'
import datetime
import math
import bisect
from sorted_collection import SortedCollection
from operator import attrgetter, methodcaller
from hours import Hours


class ToyBacklogV2:
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
        self.easy_toy_list = EasyToyBacklog(easy_toy_temp_list)
        heapq.heapify(self.variable_toy_list)
        heapq.heapify(self.hardest_toy_list)
        self.should_focus_on_hardest = False

    def get_best_fit_easy_toy(self, max_toy_duration):
        return self.easy_toy_list.peek_at_best_fit_easy_toy(max_toy_duration)

    def pop_best_fit_easy_toy(self, max_toy_duration):
        return self.easy_toy_list.pop_best_fit_easy_toy(max_toy_duration)

    def pop_variable_toy(self):
        return heapq.heappop(self.variable_toy_list)[1]

    def pop_hardest_toy(self):
        return heapq.heappop(self.hardest_toy_list)[1]

    def should_focus_on_hardest(self, target):
        if self.should_focus_on_hardest:
            return True
        if self.easy_toy_list.array_of_index_pointers[2400] < 600 * target:
            self.should_focus_on_hardest = True
            return True
        return False

    def done(self):
        return self.easy_toy_list.size == 0 and len(self.constant_rating_list) == 0 and len(
            self.variable_toy_list) == 0 and len(self.hardest_toy_list) == 0