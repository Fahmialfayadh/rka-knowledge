import heapq

class dinnerplates:
    def __init__ (self, capacity: int):
        self.capacity = capacity
        self.stacks = []
        self.available_indices = []
        self.non_empty_indices = []
    
    def push(self, val: int):
        while self.available_indices:
            idx = self.available_indices[0]
            if idx < len(self.stacks) or idx < self.capacity:
                break
            heapq.heappop(self.available_indices)

        if not self.available_indices:
            idx = len(self.stacks)
            self.stacks.append([])
            heapq.heappush(self.available_indices, idx)
        else:
            idx = self.available_indices[0]
        self.stacks[idx].append(val)
        if len(self.stacks[idx]) == self.capacity:
            heapq.heappop(self.available_indices)
        if len(self.stacks[idx]) == 1:
            heapq.heappush(self.non_empty_indices, -idx)
        
    def pop(self) -> int:
        while self.non_empty_indices:
            idx = -self.non_empty_indices[0]
            if idx < len(self.stacks) and self.stacks[idx]:
                break
            heapq.heappop(self.non_empty_indices)
            
        if not self.non_empty_indices:
            return -1
        
        idx = -self.non_empty_indices[0]
        val = self.stacks[idx].pop()
        
        # jika baru saja berkurang dari penuh, tandai sebagai available
        if len(self.stacks[idx]) == self.capacity - 1:
            heapq.heappush(self.available_indices, idx)
            
        return val

    def popAtStack(self, idx: int):
        if self.stacks[idx]:
            val = self.stacks[idx].pop()
        else:
            return -1
        
        if len(self.stacks[idx]) == self.capacity -1:
            heapq.heappush(self.available_indices, idx)
        
        if self.stacks[idx]:
            heapq.heappush(self.non_empty_indices, -idx)
        return val
