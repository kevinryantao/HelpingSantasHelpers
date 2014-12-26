__author__ = 'ktao'

from sorted_collection import SortedCollection
from operator import attrgetter


class ElvesReady:

    def __init__(self):
        self.training_elf_list = SortedCollection(key=attrgetter('rating'))
        self.high_performance_elf_list = []

    def get_elf_with_best_fit_rating(self, rating):
        return self.training_elf_list.find_ge(rating)

    def add_elf(self, elf):
        if elf.rating > 3.95:
            self.high_performance_elf_list.append(elf)
        else:
            self.training_elf_list.insert(elf)

    def add_elves(self, elves):
        for elf in elves:
            self.add_elf(elf)

    def remove_from_training_list(self, elf):
        self.training_elf_list.remove(elf)

    def remove_from_high_performance_list(self, elf):
        self.high_performance_elf_list.remove(elf)

    #todo: remove elves that are chosen.