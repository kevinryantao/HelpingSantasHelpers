import csv
import datetime

__author__ = 'ktao'

class SolutionWriter:
    def __init__(self, soln_file):
        self.w = open(soln_file, 'wt')
        self.wcsv = csv.writer(self.w)
        self.wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])
        self.ref_time = datetime.datetime(2014, 1, 1, 0, 0)

    def write(self, toy, elf, work_start_time, work_duration):
        tt = self.ref_time + datetime.timedelta(seconds=60 * work_start_time)
        time_string = " ".join([str(tt.year), str(tt.month), str(tt.day), str(tt.hour), str(tt.minute)])
        self.wcsv.writerow([toy.id, elf.id, time_string, work_duration])

    def close(self):
        self.w.close()