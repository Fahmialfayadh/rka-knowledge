class Solution:
    def dfs(self, grid, i, j, old_color, new_color):
        n = len(grid)
        m = len(grid[0])
        if i < 0 or i >=n or j<0 or j >= m or grid[i][j] != old_color:
            return grid
        else:
            grid[i][j] = new_color
            self.dfs(grid, i+1, j, old_color, new_color)
            self.dfs(grid, i-1, j, old_color, new_color)
            self.dfs(grid, i, j+1, old_color, new_color)
            self.dfs(grid, i, j-1, old_color, new_color)

    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        old_color = image[sr][sc]
        if old_color == color:
            return image
        else:
            self.dfs(image, sr, sc, old_color, color)
            return image
