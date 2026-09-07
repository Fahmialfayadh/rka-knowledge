M, N, X, Y = list(map(int, input().split()))
grid = []
for i in range(M):
    baris = list(map(int, input().split()))
    grid.append(baris)

for i in range(X):
    for j in range(Y):
        if i == 0 and j == 0:
            continue
        
        path_top = 0
        path_left = 0
        
        # Cek apakah ada jalan dari ATAS? (artinya bukan baris pertama)
        if i > 0:
            path_top = grid[i-1][j]
            
        # Cek apakah ada jalan dari KIRI? (artinya bukan kolom pertama)
        if j > 0:
            path_left = grid[i][j-1]
        if i == 0:
            grid[i][j] += path_left
        elif j == 0:
            grid[i][j] += path_top
        else:
            # Ambil yang paling besar antara path_top atau path_left
            if path_top > path_left:
                grid[i][j] += path_top
            else:
                grid[i][j] += path_left


print(grid[X-1][Y-1])