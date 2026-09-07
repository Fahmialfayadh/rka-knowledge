from collections import deque
from bisect import bisect_left, bisect_right
from sortedcontainers import SortedList

class Router:

    def __init__(self, memoryLimit: int):
        self.memoryLimit = memoryLimit
        self.queue = deque()
        self.seen = set()
        # maintain sorted timestamps per destination buat bisect cepat
        #fungsinya buat ngurutin timestamp per destination
        self.destination_timestamps = {}

    def addPacket(self, source, destination, timestamp):
        key = (source, destination, timestamp)
        if key in self.seen:
            return False
        if len(self.queue) == self.memoryLimit:
            removed = self.queue.popleft()
            self.seen.discard(removed)
            # hapooss timestamp dari sorted list destination yang di-evict
            removed_source, removed_destination, removed_timestamp = removed
            self.destination_timestamps[removed_destination].remove(removed_timestamp)
        self.queue.append(key)
        self.seen.add(key)

        # add timestamp ke sorted list untuk destination 
        if destination not in self.destination_timestamps:
            self.destination_timestamps[destination] = SortedList() #biar otomatis ke sort saaat di append

        self.destination_timestamps[destination].add(timestamp)

        return True

    def forwardPacket(self):
        if self.queue:
            removed = self.queue.popleft()
            self.seen.discard(removed)
            removed_source, removed_destination, removed_timestamp = removed
            self.destination_timestamps[removed_destination].remove(removed_timestamp)
            return list(removed)
        return []

    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        if destination not in self.destination_timestamps:
            return 0
        sorted_times = self.destination_timestamps[destination]
        # pake bisect biar g anu
        idx_start = sorted_times.bisect_left(startTime)
        idx_end = sorted_times.bisect_right(endTime)
        return idx_end - idx_start