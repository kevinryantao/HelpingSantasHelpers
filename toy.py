import datetime
import math
from hours import Hours


class Toy:
    def __init__(self, toyid, arrival, duration):
        self.reference_start_time = datetime.datetime(2014, 1, 1, 0, 0)  # set when elf starts working on toy
        self.id = toyid
        self.arrival_minute = Hours.convert_to_minute(arrival)
        self.duration = int(duration)
        self.completed_minute = 0

    def outside_toy_start_period(self, start_minute):
        """ Checks that work on toy does not start outside of the allowed starting period.
        :param start_minute: minute the work is scheduled to start
        :return: True of outside of allowed starting period, False otherwise
        """
        return start_minute < self.arrival_minute

    def is_complete(self, start_minute, elf_duration, rating):
        """ Determines if the toy is completed given duration of work and elf's productivity rating
        :param start_minute: minute work started
        :param elf_duration: duration of work in minutes
        :param rating: elf's productivity rating
        :return: Boolean
        """
        if self.duration / rating <= elf_duration:
            self.completed_minute = start_minute + int(math.ceil(self.duration / rating))
            return True
        else:
            return False

    def penalty_assuming_4elf_and_max_sanctioned(self):
        """
        This calculates the penalty if for this toy if worked on by a 4.0 rating elf starting at the beginning of the day
        :return:
        """
        time_taken = self.duration // 4
        mod24hours = time_taken % (24 * 60)
        whole_days = time_taken // (24 * 60)
        sanctioned_min = whole_days * (10 * 60) + max(mod24hours, 10 * 60)
        unsanctioned_min = time_taken - sanctioned_min
        penalty = max(0.0625, (1.02 ** (sanctioned_min / 60.0)) * 0.9 ** (unsanctioned_min / 60.0))
        return penalty

    def __lt__(self, other):
        if (isinstance(other, Toy)):
            return self.id < other.id
        else:
            return False
