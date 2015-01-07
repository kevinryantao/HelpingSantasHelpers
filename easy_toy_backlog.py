class EasyToyBacklog:
    def __init__(self, initial_toys):
        self.array_of_toys = []
        self.array_of_index_pointers = [None] * 2401
        self.size = len(initial_toys)

        for i in range(0, 2401, 1):
            self.array_of_toys.append([])
            self.array_of_index_pointers[i] = i

        for toy in initial_toys:
            self.array_of_toys[toy.duration].append(toy)

    def __sizeof__(self):
        return self.size

    def verify_target_duration(self, max_toy_duration, target_duration):
        while target_duration > 0 and len(self.array_of_toys[target_duration]) == 0:
            target_duration -= 1
        for i in range(target_duration, max_toy_duration + 1):
            self.array_of_index_pointers[i] = target_duration
        return target_duration

    def peek_at_best_fit_easy_toy(self, max_toy_duration):
        max_toy_duration = int(max_toy_duration)
        target_duration = self.array_of_index_pointers[max_toy_duration]
        target_duration = self.verify_target_duration(max_toy_duration, target_duration)
        if len(self.array_of_toys[target_duration]) > 0:
            return self.array_of_toys[target_duration][-1]
        else:
            return None

    def pop_best_fit_easy_toy(self, max_toy_duration):
        max_toy_duration = int(max_toy_duration)
        'first see what the index pointer points to'
        target_duration = self.array_of_index_pointers[max_toy_duration]
        target_duration = self.verify_target_duration(max_toy_duration, target_duration)
        if len(self.array_of_toys[target_duration]) > 0:
            self.size -= 1
            return self.array_of_toys[target_duration].pop()
        else:
            return None

    def all_toys(self):
        all = []
        for i in range(0, len(self.array_of_toys)):
            list = self.array_of_toys[i]
            for toy in list:
                all.append(toy)
        return all

    def clear(self):
        for i in range(0, len(self.array_of_toys)):
            self.array_of_toys[i].clear()
        self.size = 0

