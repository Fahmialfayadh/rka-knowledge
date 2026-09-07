class Solution:
    def findCenter(self, edges: List[List[int]]) -> int:
        # Center pasti muncul di edge[0] dan edge[1]
        # Cek apakah node dari edge[0] ada di edge[1]
        if edges[0][0] in edges[1]:
            return edges[0][0]
        return edges[0][1]
#https://leetcode.com/problems/find-center-of-star-graph/