__author__ = 'ktao'
import datetime
import math
import bisect
from sorted_collection import SortedCollection
from operator import attrgetter
from hours import Hours

class ToyBacklog:
    def __init__(self):
        self.sorted_toy_list = SortedCollection(key=attrgetter('duration'))

    def get_best_fit_toy(self, max_toy_duration):
        return self.sorted_toy_list.find_le(max_toy_duration)

    def add_toy_to_backlog(self, toy):
        return self.sorted_toy_list.insert(toy)

    def add_toys_to_backlog(self, toys):
        for toy in toys:
            self.add_toy_to_backlog(toy)