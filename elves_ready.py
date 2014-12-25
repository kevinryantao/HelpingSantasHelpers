__author__ = 'ktao'

from sorted_collection import SortedCollection
from operator import attrgetter


class ElvesReady:

    def __init__(self):
        self.sorted_elf_list = SortedCollection(key=attrgetter('rating'))

    def get_elf_with_best_fit_rating(self, rating):
        return self.sorted_elf_list.find_ge(rating)

    def add_elf(self, elf):
        self.sorted_elf_list.insert(elf)

    def add_elves(self, elves):
        for elf in elves:
            self.add_elf(elf)
