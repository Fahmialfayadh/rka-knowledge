n, m = map(int, input().split())
grid = []
for _ in range(n):
    row = list(input())
    grid.append(row)

# Visited array
visited = [[False] * m for _ in range(n)]

def dfs_iterative(start_x, start_y):
    stack = [(start_x, start_y)]
    visited[start_x][start_y] = True
    
    while stack:
        x, y = stack.pop()
        # Check 4 directions
        # Down
        if x + 1 < n and grid[x + 1][y] == '.' and not visited[x + 1][y]:
            visited[x + 1][y] = True
            stack.append((x + 1, y))
        # Up
        if x - 1 >= 0 and grid[x - 1][y] == '.' and not visited[x - 1][y]:
            visited[x - 1][y] = True
            stack.append((x - 1, y))
        # Right
        if y + 1 < m and grid[x][y + 1] == '.' and not visited[x][y + 1]:
            visited[x][y + 1] = True
            stack.append((x, y + 1))
        # Left
        if y - 1 >= 0 and grid[x][y - 1] == '.' and not visited[x][y - 1]:
            visited[x][y - 1] = True
            stack.append((x, y - 1))

# rooms
rooms = 0
for i in range(n):
    for j in range(m):
        if grid[i][j] == '.' and not visited[i][j]:
            rooms += 1
            dfs_iterative(i, j)

print(rooms)