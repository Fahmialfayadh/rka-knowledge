from collections import deque
from typing import List

class Solution:
    def minimumCoins(self, prices: List[int]) -> int:
        n = len(prices)
        # dp[i] stores the minimum cost to get all fruits from index i to the end
        dp = [0] * (n + 1)
        
        # Deque will store indices in a way that their corresponding dp values 
        # are monotonically increasing from left to right.
        q = deque()
        
        # Traverse backwards
        for i in range(n - 1, -1, -1):
            # 1. Add the next available state (i + 1) to the monotonic queue
            # We pop elements from the right if they have a greater or equal dp value.
            # They are useless because dp[i+1] is both cheaper/equal AND expires later.
            while q and dp[i + 1] <= dp[q[-1]]:
                q.pop()
            
            q.append(i + 1)
            
            # 2. Expire elements from the left if they fall out of our valid "free" window
            # The window of free fruits ends at 2i + 1, so the next bought fruit can be at most 2i + 2.
            while q and q[0] > 2 * i + 2:
                q.popleft()
                
            # 3. Calculate dp[i] using the best available future state (front of the queue)
            dp[i] = prices[i] + dp[q[0]]
            
        # To get the ball rolling, we are forced to buy the very first fruit (index 0)
        return dp[0]