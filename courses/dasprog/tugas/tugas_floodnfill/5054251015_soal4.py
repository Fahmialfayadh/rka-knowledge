

n, m = map(int, input().split())
grid = [list(input().rstrip()) for _ in range(n)]
start = end = None
for i in range(n):
    for j in range(m):
        if grid[i][j] == 'A':
            start = (i, j)
        elif grid[i][j] == 'B':
            end = (i, j)

# bfs setup
visited = [[False] * m for _ in range(n)]
parent = [[None] * m for _ in range(n)]  # simpan arah datang
direction_char = { (1,0): 'D', (-1,0): 'U', (0,1): 'R', (0,-1): 'L' }

sx, sy = start
ex, ey = end

nodes = [(sx, sy)]
visited[sx][sy] = True
head = 0
dirs = [(1,0,'D'), (-1,0,'U'), (0,1,'R'), (0,-1,'L')]

while head < len(nodes):
    x, y = nodes[head]
    head += 1

    if (x, y) == (ex, ey):
        break

    for dx, dy, ch in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m:
            if not visited[nx][ny] and grid[nx][ny] != '#':
                visited[nx][ny] = True
                parent[nx][ny] = (x, y, ch)
                nodes.append((nx, ny))

if not visited[ex][ey]:
    print("NO")
    exit()

# reconstruct path
path = []
cx, cy = ex, ey
while (cx, cy) != (sx, sy):
    px, py, ch = parent[cx][cy]
    path.append(ch)
    cx, cy = px, py

path.reverse()

print("YES")
print(len(path))
print("".join(path))
