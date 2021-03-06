__author__ = 'ktao'
import math
import hours
from toy_backlog import ToyBacklog
from toy_loader import ToyLoader
from elves_ready import ElvesReady


class Scheduler:
    def __init__(self, TARGET, num_elves):
        self.rating_threshold = 3.95
        self.hrs = hours.Hours()
        self.target_for_hardest = TARGET
        self.focus_on_hardest = False
        self.num_elves = num_elves

    def schedule(self, toy_backlog, elves_ready, busy_elves_heap, current_time, solution_writer, toy_loader):

        minutes_left_in_day = self.hrs.minutes_left_in_sanctioned_day(current_time)

        self.focus_on_hardest = toy_backlog.focus_on_hardest(self.target_for_hardest)

        elves_toys_paired_off = 0

        # 1. check if < 3.95
        # a. calculate based on current_time what's the effective duration of toy that can be built
        #   b. if >3.28 calculate based on rating, how much time left to become 4
        #       based on min of those two numbers find toy that's the best fit
        #       find if that toy has a better fit

        for elf in elves_ready.high_performance_elf_list[:]:
            # if it's the start of the day, then go for constants first, then variables
            # else do hardest toys if available
            # else put self in training list and pick up old jobs there.
            if self.focus_on_hardest and len(toy_backlog.hardest_toy_list) > 0:
                toy = self.get_hardest_toys(toy_backlog)
            else:
                toy = self.get_toy_for_4rating(minutes_left_in_day, toy_backlog, toy_loader)
            if toy is not None:
                # pair off the elf and toy
                busy_elves_heap.assign_toy_to_elf(elf, toy, current_time, solution_writer)

                # remove the elf and toy
                elves_ready.remove_from_high_performance_list(elf)
                elves_toys_paired_off += 1

        for elf in elves_ready.training_elf_list[:]:
            hard_toy = False
            toy = None
            if toy_backlog.get_best_fit_easy_toy(600*self.target_for_hardest) is None and len(toy_backlog.constant_rating_list) == 0 and elf.rating < self.target_for_hardest*1.2:
                if len(toy_backlog.hardest_toy_list) > 0:
                    toy = self.get_hardest_toys(toy_backlog)
                    hard_toy = True
                elif len(toy_backlog.variable_toy_list) > 0:
                    toy = toy_backlog.pop_variable_toy()
                    hard_toy = True
                elif toy_backlog.easy_toy_list.size > 0:
                    toy = toy_backlog.pop_best_fit_easy_toy(2400)
                    hard_toy = True
            elif self.focus_on_hardest and len(toy_backlog.hardest_toy_list) > 0 and len(toy_backlog.constant_rating_list) == 0:
                if self.target_for_hardest <= elf.rating:
                    toy = self.get_hardest_toys(toy_backlog)
                    hard_toy = True
                else:
                    target_toy_duration = minutes_left_in_day * elf.rating
                    toy = toy_backlog.get_best_fit_easy_toy(target_toy_duration)
            elif len(toy_backlog.hardest_toy_list) > 0 and len(toy_backlog.constant_rating_list) == 0:
                if self.target_for_hardest <= elf.rating and (elf.rating < self.target_for_hardest * 1.2 or elf.id <= self.num_elves * .96):
                    toy = self.get_hardest_toys(toy_backlog)
                    hard_toy = True
                elif elf.rating > self.target_for_hardest * 1.2:
                    if minutes_left_in_day > 400:
                        target_toy_duration = minutes_left_in_day * elf.rating
                        toy = toy_backlog.get_best_fit_easy_toy(target_toy_duration)
                    else:
                        toy = None
                else:
                    target_toy_duration = minutes_left_in_day * elf.rating
                    toy = toy_backlog.get_best_fit_easy_toy(target_toy_duration)
            elif self.focus_on_hardest and len(toy_backlog.hardest_toy_list) == 0 and len(toy_backlog.variable_toy_list) > 0:
                if self.target_for_hardest <= elf.rating:
                    toy = toy_backlog.pop_variable_toy()
                    hard_toy = True
                else:
                    target_toy_duration = minutes_left_in_day * elf.rating
                    toy = toy_backlog.get_best_fit_easy_toy(target_toy_duration)
            elif len(toy_backlog.hardest_toy_list) == 0 and len(toy_backlog.variable_toy_list) > 0:
                if minutes_left_in_day > 500:
                    target_toy_duration = minutes_left_in_day * elf.rating
                    toy = toy_backlog.get_best_fit_easy_toy(target_toy_duration)
                else:
                    toy = None

            else:
                target_toy_duration = minutes_left_in_day * elf.rating
                toy = toy_backlog.get_best_fit_easy_toy(target_toy_duration)

            if toy is not None:
                # remove the elf and toy
                elves_ready.remove_from_training_list(elf)
                if not hard_toy:
                    toy = toy_backlog.pop_best_fit_easy_toy(toy.duration)

                # pair off the elf and toy
                busy_elves_heap.assign_toy_to_elf(elf, toy, current_time, solution_writer)
                elves_toys_paired_off += 1

                #if elves_toys_paired_off == 0 and len(elves_ready.training_elf_list) > 499:
                #   print("No elves or toys paired")
                #  for elf in elves_ready.training_elf_list[:]:
                #     print('elf id:{0}, elf rating:{1}'.format(elf.id, elf.rating))
                #for toy in toy_backlog.easy_toy_list[:]:
                #   print('toy id:{0}, toy duration:{1}'.format(toy.id, toy.duration))

        return elves_toys_paired_off


    def clean_up(self, toys_left_at_end, elves_ready, busy_elves_heap, current_time, solution_writer):
        # this is the situation where there's no more new toys, and no more easy toys.
        length_of_toy_backlog = len(toys_left_at_end)
        length_of_ready_elves = len(elves_ready.high_performance_elf_list) + len(elves_ready.training_elf_list)
        elves = []
        for elf in elves_ready.training_elf_list:
            elves.append(elf)
        for elf in elves_ready.high_performance_elf_list:
            elves.append(elf)
        elves_toys_paired_off = 0

        num_pairs = min(len(elves), len(toys_left_at_end))
        for i in range(0, num_pairs):
            elf = elves.pop()
            toy = toys_left_at_end.pop()
            self.remove_elf(elf, elves_ready)
            # pair off the elf and toy
            busy_elves_heap.assign_toy_to_elf(elf, toy, current_time, solution_writer)
            elves_toys_paired_off += 1

        return elves_toys_paired_off

    def get_toy_for_4rating(self, minutes_left_in_day, toy_backlog, toy_loader):
        if minutes_left_in_day > 599:
            if len(toy_backlog.constant_rating_list) > 0:
                return toy_backlog.constant_rating_list.pop()
            if len(toy_backlog.variable_toy_list) > 0:
                return toy_backlog.pop_variable_toy()
        if toy_loader.done() and len(toy_backlog.constant_rating_list) == 0 and len(toy_backlog.variable_toy_list) == 0:
            if len(toy_backlog.hardest_toy_list) > 0:
                return toy_backlog.pop_hardest_toy()
            target_toy_duration = minutes_left_in_day * 4
            toy = toy_backlog.get_best_fit_easy_toy(target_toy_duration)
            if toy.duration > 520 / self.target_for_hardest:
                toy = toy_backlog.pop_best_fit_easy_toy(target_toy_duration)
                return toy
        return None

    def get_hardest_toys(self, toy_backlog):
        if len(toy_backlog.hardest_toy_list) > 0:
            return toy_backlog.pop_hardest_toy()
        return None

    def remove_elf(self, elf, elves_ready):
        if elves_ready.training_elf_list.__contains__(elf):
            elves_ready.remove_from_training_list(elf)
        elif elves_ready.high_performance_elf_list.__contains__(elf):
            elves_ready.remove_from_high_performance_list(elf)

    def remove_toy(self, toy, toy_backlog):
        if toy_backlog.constant_rating_list.__contains__(toy):
            toy_backlog.constant_rating_list.remove(toy)
        elif toy_backlog.variable_toy_list.__contains__(toy):
            toy_backlog.variable_toy_list.remove(toy)
        elif toy_backlog.hardest_toy_list.__contains__(toy):
            toy_backlog.hardest_toy_list.remove(toy)

    @staticmethod
    def calculate_minutes_to_fully_train(elf):
        multiplier_needed = 4.0 / elf.rating
        actual_minutes_needed = (math.log(multiplier_needed) / math.log(1.02)) * 60
        return actual_minutes_needed * elf.rating

    def calculate_minutes_to_train_to_target(self, elf):
        if(elf.rating >= self.target_for_hardest):
            return 0

        multiplier_needed = self.target_for_hardest / elf.rating
        actual_minutes_needed = (math.log(multiplier_needed) / math.log(1.02)) * 60
        return actual_minutes_needed * elf.rating


