from collections import deque
class RecentCounter:

    def __init__(self):
        self.countping = deque()

    def ping(self, t: int) -> int:
        self.countping.append(t)
        while self.countping[0] < t - 3000:
            self.countping.popleft()
        return len(self.countping)


# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)