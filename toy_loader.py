import csv
from toy import Toy

__author__ = 'ktao'


class ToyLoader:
    def __init__(self, file_name):
        self.f = open(file_name)
        self.file = csv.reader(self.f)
        next(self.file)  # header row
        self.lastToy = None
        self.isDone = False

    def get_toys_up_to_minute(self, minute):
        toys = []
        if self.lastToy is not None:
            if self.lastToy.arrival_minute <= minute:
                toys.append(self.lastToy)
                self.lastToy = None

        while self.lastToy is None:
            row = next(self.file, None)
            if row is not None:
                toy = Toy(row[0], row[1], row[2])
                if toy.arrival_minute <= minute:
                    toys.append(toy)
                else:
                    self.lastToy = toy
            else:
                self.isDone = True
                break

        return toys

    def done(self):
        return self.isDone

    def close(self):
        self.f.close()
