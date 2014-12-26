__author__ = 'ktao'
import math
import hours
from toy_backlog import ToyBacklog
from toy_loader import ToyLoader
from elves_ready import ElvesReady

class Scheduler:
    def __init__(self):
        self.rating_threshold = 3.95
        self.hrs = hours.Hours()

    def schedule(self, toy_backlog, elves_ready, busy_elves_heap, current_time, solution_writer):

        minutes_left_in_day = self.hrs.minutes_left_in_sanctioned_day(current_time)

        # 1. check if < 3.95
        #   a. calculate based on current_time what's the effective duration of toy that can be built
        #   b. if >3.28 calculate based on rating, how much time left to become 4
        #       based on min of those two numbers find toy that's the best fit
        #       find if that toy has a better fit

        for elf in elves_ready.high_performance_elf_list[:]:
            # if it's the start of the day, then go for constants first, then variables
            # else do hardest toys if available
            # else put self in training list and pick up old jobs there.
            toy = self.get_toy(minutes_left_in_day, toy_backlog)
            if toy is not None:
                # pair off the elf and toy
                line = busy_elves_heap.assign_toy_to_elf(elf, toy, current_time, solution_writer)
                solution_writer.write_line(line)
                # remove the elf and toy
                elves_ready.remove_from_high_performance_list(elf)
            else:
                elves_ready.training_elf_list.insert(elf)
                elves_ready.remove_from_high_performance_list(elf)

        for elf in elves_ready.training_elf_list[:]:

            if (elf.rating > 3.28) and (elf.rating < self.rating_threshold):
                target_toy_duration = self.calculate_minutes_to_fully_train(elf)
            else:
                target_toy_duration = minutes_left_in_day * elf.rating

            toy = toy_backlog.get_best_fit_easy_toy(target_toy_duration)

            if toy is not None:
                # remove the elf and toy
                elves_ready.remove_from_training_list(elf)
                toy_backlog.easy_toy_list.remove(toy)

                # pair off the elf and toy
                busy_elves_heap.assign_toy_to_elf(elf, toy, current_time, solution_writer)

        return None



    def get_toy(self, minutes_left_in_day, toy_backlog):
        if minutes_left_in_day > 540:
            if len(toy_backlog.constant_rating_list) > 0:
                return toy_backlog.constant_rating_list.pop()
            elif len(toy_backlog.variable_toy_list) > 0:
                return toy_backlog.variable_toy_list.pop()
        if len(toy_backlog.hardest_toy_list) > 0:
                return toy_backlog.hardest_toy_list.pop()
        return None

    @staticmethod
    def calculate_minutes_to_fully_train(elf):
        multiplier_needed = 4.0 / elf.rating
        actual_minutes_needed = math.log(multiplier_needed) / math.log(1.02 / 60)
        return actual_minutes_needed * elf.rating


