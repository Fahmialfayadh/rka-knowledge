import sys
sys.setrecursionlimit(2000)

MOD = 10**9 + 7
try:
    n_input = input()
except EOFError:
    n_input = "0"

grid = []
try:
    while True:
        line = input()
        grid.append(list(line))
except EOFError:
    pass

n = len(grid)
# cari kolom terpanjang dan jadiknnya sebagai panjang dp
max_cols = 0
if n > 0:
    for row in grid:
        max_cols = max(max_cols, len(row))

if n == 0 or max_cols == 0:
    print(0)
else:
    m = max_cols
    if grid[0][0] == '*' or grid[n-1][len(grid[n-1])-1] == '*':
        print(0)
    else:
        # dp
        dp = [[0] * m for _ in range(n)]
        dp[0][0] = 1
        
        # baris pertama
        for j in range(1, min(m, len(grid[0]))):
            if grid[0][j] != '*':
                dp[0][j] = dp[0][j-1]
        
        # kolom pertama
        for i in range(1, n):
            if len(grid[i]) > 0 and grid[i][0] != '*':
                dp[i][0] = dp[i-1][0]
        
        for i in range(1, n):
            for j in range(1, min(m, len(grid[i]))):
                if grid[i][j] != '*':
                    dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
        
        print(dp[n-1][len(grid[n-1])-1])