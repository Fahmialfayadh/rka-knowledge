from collections import deque
class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        queue = deque()
        for x in senate:
            queue.append(x)
        while queue:
            sen1 = queue.popleft()
            target = 'D' if sen1 == 'R' else 'R'

            if target in queue:
                queue.remove(target)
                queue.append(sen1)
            else:
                return "Radiant" if sen1 == 'R' else "Dire"
            
class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        queue = deque()
        for x in senate:
            queue.append(x)
        while queue:
            sen1 = queue.popleft()
            target = 'D' if sen1 == 'R' else 'R'

            if target in queue:
                queue.remove(target)
                queue.append(sen1)
            else:
                return "Radiant" if sen1 == 'R' else "Dire"
            