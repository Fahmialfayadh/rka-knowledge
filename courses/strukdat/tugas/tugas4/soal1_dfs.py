class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        move = ((1, 0), (-1, 0), (0,1), (0,-1))
        rows, cols = len(grid), len(grid[0])
        perimeter = 0
        island = 0
        visited = set()
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1:
                    stack = [(i,j)]
                    visited.add((i,j))
                    while stack:
                        curr_row, curr_cols = stack.pop()
                        for mi, mj in move:
                            ni, nj = curr_row+mi, curr_cols+mj
                            if ni >= rows or ni < 0 or nj >= cols or nj < 0 or grid[ni][nj] == 0:
                                perimeter += 1

                        island += 1
        print()
        return perimeter
        
