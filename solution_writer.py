import csv
import datetime
from hours import Hours

__author__ = 'ktao'

class SolutionWriter:
    def __init__(self, soln_file):
        self.w = open(soln_file, 'wt')
        self.wcsv = csv.writer(self.w)
        self.wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])
        self.ref_time = datetime.datetime(2014, 1, 1, 0, 0)
        self.hours = Hours()

    def write(self, toy, elf, work_start_time, work_duration):
        time_string = self.hours.get_time_string(work_start_time)
        self.wcsv.writerow([toy.id, elf.id, time_string, work_duration])

    def close(self):
        self.w.close()