import collections
class Solution(object):
    def maxSlidingWindow(self, nums, k):
        max_indices = collections.deque() #nyimpan index index max dari window
        out = []

        for i, n in enumerate(nums):
            while max_indices and nums[max_indices[-1]] < n: #cek kalau max index pada window tersebut lebih kecil dari angka yg skrg maka dipop
                max_indices.pop()
                
            max_indices.append(i) 

            if max_indices[0] == i - k: #buang index yg udah lewat (kadaluarsa)
                max_indices.popleft()

            if i+1>=k: # apakah angka yg udah diproses udh sama atau lebih dari batas window blom
                out.append(nums[max_indices[0]]) #kalau udah, append max num pada window ke out
        return out

#https://leetcode.com/problems/sliding-window-maximum/submissions/1962699147
