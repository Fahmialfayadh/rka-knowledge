class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        move = ((1, 0), (-1, 0), (0,1), (0,-1))
        rows, cols = len(grid), len(grid[0])
        perimeter = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    for mi, mj in move:
                        ni, nj = i+mi, j+mj
                        if ni >= rows or ni < 0 or nj >= cols or nj < 0 or grid[ni][nj] == 0:
                            perimeter += 1
        return perimeter
#https://leetcode.com/problems/island-perimeter/submissions/1973428537/
