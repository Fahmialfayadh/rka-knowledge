import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Konfigurasi State (0 melambangkan ubin kosong)
INITIAL_STATE = np.array([[0, 1, 3], [4, 2, 5], [7, 8, 6]])
GOAL_STATE = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

def find_blank(state):
    return tuple(np.argwhere(state == 0)[0])

def get_neighbors(state):
    neighbors = []
    r, c = find_blank(state)
    # Atas, Bawah, Kiri, Kanan
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = state.copy()
            new_state[r, c], new_state[nr, nc] = new_state[nr, nc], new_state[r, c]
            neighbors.append(new_state)
    return neighbors

def dls(current, goal, depth, path):
    if np.array_equal(current, goal):
        return path
    if depth <= 0:
        return None
    
    for neighbor in get_neighbors(current):
        # Hindari siklus sederhana (backtracking ke state sebelumnya)
        if any(np.array_equal(neighbor, p) for p in path):
            continue
            
        result = dls(neighbor, goal, depth - 1, path + [neighbor])
        if result is not None:
            return result
    return None

def ids(start, goal, max_depth=20):
    for depth in range(max_depth):
        print(f"Checking depth limit: {depth}...")
        result = dls(start, goal, depth, [start])
        if result is not None:
            return result
    return None

# Jalankan IDS
solution_path = ids(INITIAL_STATE, GOAL_STATE)

if solution_path:
    print(f"Solusi ditemukan dalam {len(solution_path)-1} langkah!")
    
    # --- BAGIAN ANIMASI ---
    fig, ax = plt.subplots(figsize=(5, 5))
    
    def update(frame):
        ax.clear()
        state = solution_path[frame]
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-0.5, 2.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.invert_yaxis() # Biar index [0,0] di kiri atas
        
        for i in range(3):
            for j in range(3):
                val = state[i, j]
                color = 'white' if val != 0 else 'gray'
                # Gambar kotak
                rect = plt.Rectangle((j-0.5, i-0.5), 1, 1, facecolor=color, edgecolor='black', lw=2)
                ax.add_patch(rect)
                # Gambar angka
                if val != 0:
                    ax.text(j, i, str(val), fontsize=30, ha='center', va='center', fontweight='bold')
        
        ax.set_title(f"IDS Solve - Step: {frame}", fontsize=15)

    ani = animation.FuncAnimation(fig, update, frames=len(solution_path), interval=800, repeat=True)
    plt.show()
else:
    print("Solusi tidak ditemukan dalam batas kedalaman.")