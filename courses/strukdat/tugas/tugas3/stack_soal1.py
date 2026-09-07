import heapq

class DinnerPlates:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.stacks = []
        self.available = []
        self.non_empty = [] 

    def push(self, val: int) -> None:
        while self.available:
            idx = self.available[0]
            if idx < len(self.stacks) and len(self.stacks[idx]) < self.capacity:
                break
            heapq.heappop(self.available)

        if not self.available:
            idx = len(self.stacks)
            self.stacks.append([])
            heapq.heappush(self.available, idx)
        else:
            idx = self.available[0]

        self.stacks[idx].append(val)
        if len(self.stacks[idx]) == self.capacity:
            heapq.heappop(self.available)
        heapq.heappush(self.non_empty, -idx)

    def pop(self) -> int:
        while self.non_empty:
            idx = -self.non_empty[0]
            if idx < len(self.stacks) and self.stacks[idx]:
                break
            heapq.heappop(self.non_empty)

        if not self.non_empty:
            return -1
        
        idx = -self.non_empty[0]
        val = self.stacks[idx].pop()
        if len(self.stacks[idx]) == self.capacity - 1:
            heapq.heappush(self.available, idx)

        return val

    def popAtStack(self, index: int) -> int:
        if index >= len(self.stacks) or not self.stacks[index]:
            return -1
        val = self.stacks[index].pop()
        if len(self.stacks[index]) == self.capacity - 1:
            heapq.heappush(self.available, index)
        if self.stacks[index]:
            heapq.heappush(self.non_empty, -index)

        return val
#https://leetcode.com/problems/dinner-plate-stacks/solutions/6805564/simple-python-solution-beats-100-by-user-ioln 
