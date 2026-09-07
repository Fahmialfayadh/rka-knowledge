import pygame
import sys

# ==================== KONFIGURASI PUZZLE ====================
START = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]
GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# ==================== WARNA ====================
BLACK = (18, 18, 24)
DARK_BG = (28, 28, 38)
PANEL_BG = (35, 35, 48)
TILE_BG = (55, 55, 75)
WHITE = (230, 230, 240)
GRAY = (120, 120, 140)
CYAN = (80, 200, 255)
YELLOW = (255, 220, 60)
RED = (255, 80, 80)
GREEN = (80, 230, 120)
MAGENTA = (200, 100, 255)
DARK_GREEN = (40, 120, 60)
ORANGE = (255, 160, 50)

# Warna tile per mode
MODE_COLORS = {
    "exploring": (70, 65, 20),      # kuning gelap
    "deadend": (80, 30, 30),         # merah gelap
    "backtrack": (70, 30, 80),       # magenta gelap
    "solution": (25, 70, 40),        # hijau gelap
    None: TILE_BG,
}
MODE_BORDER = {
    "exploring": YELLOW,
    "deadend": RED,
    "backtrack": MAGENTA,
    "solution": GREEN,
    None: GRAY,
}
MODE_STATUS_COLOR = {
    "exploring": YELLOW,
    "deadend": RED,
    "backtrack": MAGENTA,
    "solution": GREEN,
    None: WHITE,
}

# ==================== KECEPATAN ANIMASI (ms) ====================
STEP_DELAY = 300
DEADEND_DELAY = 600
BACKTRACK_DELAY = 400
SOLUTION_DELAY = 700
NEWLIMIT_DELAY = 500

# ==================== WINDOW ====================
WIDTH, HEIGHT = 900, 680
TILE_SIZE = 75
GRID_PAD = 6
GRID_X, GRID_Y = 50, 110


# ==================== VISUALIZER ====================
class PuzzleVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("8-Puzzle IDS Solver - Live Simulation")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_tile = pygame.font.SysFont("consolas", 32, bold=True)
        self.font_stat = pygame.font.SysFont("consolas", 16)
        self.font_stat_bold = pygame.font.SysFont("consolas", 16, bold=True)
        self.font_log = pygame.font.SysFont("consolas", 13)
        self.font_small = pygame.font.SysFont("consolas", 14)
        self.font_big = pygame.font.SysFont("consolas", 36, bold=True)
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def wait(self, ms):
        """Delay sambil tetap handle events agar window tidak freeze."""
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < ms:
            self.handle_events()
            self.clock.tick(60)

    def draw_header(self):
        # Header bar
        pygame.draw.rect(self.screen, PANEL_BG, (0, 0, WIDTH, 55))
        pygame.draw.line(self.screen, CYAN, (0, 55), (WIDTH, 55), 2)
        text = self.font_title.render("8-PUZZLE IDS SOLVER  —  LIVE SIMULATION", True, CYAN)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 16))

    def draw_grid(self, state, goal, mode, x, y, tile_size=None):
        if tile_size is None:
            tile_size = TILE_SIZE
        pad = GRID_PAD
        grid_total = tile_size * 3 + pad * 4

        # Grid background
        bg_rect = pygame.Rect(x - pad, y - pad, grid_total, grid_total)
        pygame.draw.rect(self.screen, (20, 20, 30), bg_rect, border_radius=8)
        border_color = MODE_BORDER.get(mode, GRAY)
        pygame.draw.rect(self.screen, border_color, bg_rect, 2, border_radius=8)

        tile_bg = MODE_COLORS.get(mode, TILE_BG)

        for r in range(3):
            for c in range(3):
                val = state[r][c]
                tx = x + c * (tile_size + pad)
                ty = y + r * (tile_size + pad)
                tile_rect = pygame.Rect(tx, ty, tile_size, tile_size)

                if val == 0:
                    # Blank tile
                    pygame.draw.rect(self.screen, (25, 25, 35), tile_rect, border_radius=6)
                    pygame.draw.rect(self.screen, (40, 40, 50), tile_rect, 1, border_radius=6)
                else:
                    # Determine tile color
                    if goal and goal[r][c] == val:
                        bg = DARK_GREEN
                        fg = GREEN
                    else:
                        bg = tile_bg
                        fg = MODE_STATUS_COLOR.get(mode, WHITE)

                    # Shadow
                    shadow = pygame.Rect(tx + 2, ty + 2, tile_size, tile_size)
                    pygame.draw.rect(self.screen, (10, 10, 15), shadow, border_radius=6)
                    # Tile
                    pygame.draw.rect(self.screen, bg, tile_rect, border_radius=6)
                    pygame.draw.rect(self.screen, fg, tile_rect, 2, border_radius=6)
                    # Number
                    num_text = self.font_tile.render(str(val), True, fg)
                    nx = tx + tile_size // 2 - num_text.get_width() // 2
                    ny = ty + tile_size // 2 - num_text.get_height() // 2
                    self.screen.blit(num_text, (nx, ny))

    def draw_stats(self, nodes, depth, limit, backtracks, status_text, mode):
        sx = 520
        sy = 110

        # Panel background
        panel = pygame.Rect(sx - 15, sy - 15, 370, 260)
        pygame.draw.rect(self.screen, PANEL_BG, panel, border_radius=8)
        pygame.draw.rect(self.screen, GRAY, panel, 1, border_radius=8)

        # Title
        t = self.font_stat_bold.render("STATISTICS", True, CYAN)
        self.screen.blit(t, (sx, sy))
        pygame.draw.line(self.screen, GRAY, (sx, sy + 22), (sx + 320, sy + 22), 1)

        # Stats
        y = sy + 35
        labels = [
            ("Nodes Explored", str(nodes)),
            ("Current Depth", f"{depth} / Limit: {limit}"),
            ("Backtracks", str(backtracks)),
        ]
        for label, value in labels:
            lt = self.font_stat.render(f"{label} :", True, GRAY)
            vt = self.font_stat_bold.render(f" {value}", True, WHITE)
            self.screen.blit(lt, (sx, y))
            self.screen.blit(vt, (sx + lt.get_width(), y))
            y += 24

        # Depth bar
        y += 5
        dt = self.font_stat.render("Depth:", True, GRAY)
        self.screen.blit(dt, (sx, y))
        bar_x = sx + 60
        bar_w = 200
        bar_h = 16
        pygame.draw.rect(self.screen, (30, 30, 40), (bar_x, y, bar_w, bar_h), border_radius=4)
        if limit > 0:
            fill_w = min(int((depth / limit) * bar_w), bar_w)
            if fill_w > 0:
                pygame.draw.rect(self.screen, YELLOW, (bar_x, y, fill_w, bar_h), border_radius=4)
        pygame.draw.rect(self.screen, GRAY, (bar_x, y, bar_w, bar_h), 1, border_radius=4)

        # Status
        y += 35
        st = self.font_stat.render("Status:", True, GRAY)
        self.screen.blit(st, (sx, y))
        sc = MODE_STATUS_COLOR.get(mode, WHITE)
        sv = self.font_stat_bold.render(f" {status_text}", True, sc)
        self.screen.blit(sv, (sx + st.get_width(), y))

    def draw_path(self, moves):
        py = 390
        px = 50
        t = self.font_small.render("Path: ", True, GRAY)
        self.screen.blit(t, (px, py))
        cx = px + t.get_width()
        max_x = WIDTH - 50
        for i, m in enumerate(moves[:15]):
            mt = self.font_small.render(m, True, CYAN)
            if cx + mt.get_width() > max_x:
                dt = self.font_small.render("...", True, GRAY)
                self.screen.blit(dt, (cx, py))
                break
            self.screen.blit(mt, (cx, py))
            cx += mt.get_width()
            if i < min(len(moves), 15) - 1:
                arrow = self.font_small.render(" > ", True, GRAY)
                self.screen.blit(arrow, (cx, py))
                cx += arrow.get_width()

    def draw_log(self, entries):
        ly = 430
        lx = 50

        # Log panel background
        panel = pygame.Rect(lx - 10, ly - 10, WIDTH - 80, 240)
        pygame.draw.rect(self.screen, PANEL_BG, panel, border_radius=8)
        pygame.draw.rect(self.screen, GRAY, panel, 1, border_radius=8)

        # Title
        t = self.font_stat_bold.render("Activity Log", True, GRAY)
        self.screen.blit(t, (lx, ly))
        pygame.draw.line(self.screen, (50, 50, 65), (lx, ly + 18), (lx + WIDTH - 100, ly + 18), 1)

        display = entries[-10:] if len(entries) > 10 else entries
        y = ly + 25
        for msg, color in display:
            prefix = self.font_log.render("[>>] ", True, GRAY)
            self.screen.blit(prefix, (lx, y))
            # Map terminal color codes to pygame colors
            c = self._resolve_color(color)
            mt = self.font_log.render(msg, True, c)
            self.screen.blit(mt, (lx + prefix.get_width(), y))
            y += 18

    def _resolve_color(self, color):
        """Resolve color — accept both tuples and names."""
        if isinstance(color, tuple):
            return color
        return WHITE

    def render_frame(self, state, goal, mode, status_text, stats, log_entries, path_moves):
        self.handle_events()
        self.screen.fill(DARK_BG)
        self.draw_header()
        self.draw_grid(state, goal, mode, GRID_X, GRID_Y)
        nodes, depth, limit, backtracks = stats
        self.draw_stats(nodes, depth, limit, backtracks, status_text, mode)
        self.draw_path(path_moves)
        self.draw_log(log_entries)
        pygame.display.flip()
        self.clock.tick(60)

    def splash_screen(self, start, goal):
        """Tampilkan splash screen, tunggu SPACE."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        waiting = False

            self.screen.fill(DARK_BG)

            # Title
            t = self.font_big.render("8-PUZZLE IDS SOLVER", True, CYAN)
            self.screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 60))

            sub = self.font_stat.render("Iterative Deepening Search Simulation", True, GRAY)
            self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 110))

            # START label
            sl = self.font_stat_bold.render("START STATE", True, YELLOW)
            self.screen.blit(sl, (150 - sl.get_width() // 2, 170))
            self.draw_grid(start, None, None, 80, 200, tile_size=55)

            # GOAL label
            gl = self.font_stat_bold.render("GOAL STATE", True, GREEN)
            self.screen.blit(gl, (WIDTH - 150 - gl.get_width() // 2, 170))
            self.draw_grid(goal, goal, "solution", WIDTH - 260, 200, tile_size=55)

            # Arrow
            arrow = self.font_big.render(">>>", True, GRAY)
            self.screen.blit(arrow, (WIDTH // 2 - arrow.get_width() // 2, 250))

            # Info
            info_lines = [
                "Algoritma mencoba path sedalam mungkin (DFS)",
                "Kalau buntu, backtrack ke alternatif lain",
                "Depth limit naik bertahap (Iterative Deepening)",
            ]
            y = 420
            for line in info_lines:
                it = self.font_small.render(f"• {line}", True, GRAY)
                self.screen.blit(it, (WIDTH // 2 - it.get_width() // 2, y))
                y += 22

            # Press space
            blink = pygame.time.get_ticks() % 1000 < 600
            if blink:
                pt = self.font_stat_bold.render("Press SPACE to begin simulation", True, WHITE)
                self.screen.blit(pt, (WIDTH // 2 - pt.get_width() // 2, 540))

            pygame.display.flip()
            self.clock.tick(30)

    def summary_screen(self, nodes, backtracks, steps):
        """Layar summary akhir."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

            self.screen.fill(DARK_BG)

            t = self.font_big.render("PUZZLE SOLVED!", True, GREEN)
            self.screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 150))

            # Divider
            pygame.draw.line(self.screen, GREEN, (200, 210), (700, 210), 2)

            stats = [
                ("Total Nodes Explored", str(nodes)),
                ("Total Backtracks", str(backtracks)),
                ("Solution Steps", str(steps)),
            ]
            y = 250
            for label, val in stats:
                lt = self.font_stat.render(f"{label} :", True, GRAY)
                vt = self.font_stat_bold.render(f"  {val}", True, WHITE)
                cx = WIDTH // 2 - (lt.get_width() + vt.get_width()) // 2
                self.screen.blit(lt, (cx, y))
                self.screen.blit(vt, (cx + lt.get_width(), y))
                y += 30

            pygame.draw.line(self.screen, GREEN, (200, y + 10), (700, y + 10), 2)

            blink = pygame.time.get_ticks() % 1000 < 600
            if blink:
                pt = self.font_small.render("Press any key to exit", True, GRAY)
                self.screen.blit(pt, (WIDTH // 2 - pt.get_width() // 2, y + 40))

            pygame.display.flip()
            self.clock.tick(30)


# ==================== PUZZLE SOLVER ====================
class PuzzleSolver:
    def __init__(self, start, goal, vis):
        self.start = start
        self.goal = goal
        self.vis = vis
        self.nodes_explored = 0
        self.backtrack_count = 0
        self.current_depth_limit = 0
        self.log = []

    def find_blank(self, state):
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    return r, c

    def get_neighbors(self, state):
        neighbors = []
        r, c = self.find_blank(state)
        moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        for dr, dc, move_name in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_state = [row[:] for row in state]
                new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
                neighbors.append((new_state, move_name))
        return neighbors

    def add_log(self, message, color=WHITE):
        self.log.append((message, color))

    def get_stats(self, depth):
        return (self.nodes_explored, depth, self.current_depth_limit, self.backtrack_count)

    def show(self, state, path, mode, status_text):
        self.nodes_explored += 1
        depth = len(path) - 1
        path_moves = [m for _, m in path]
        self.vis.render_frame(state, self.goal, mode, status_text,
                              self.get_stats(depth), self.log, path_moves)

    def dls(self, current, goal, depth, path):
        """Depth-Limited Search dengan visualisasi Pygame."""
        self.show(current, path, "exploring", "EXPLORING...")
        self.add_log(f"Depth {len(path)-1}: Exploring (move: {path[-1][1]})", YELLOW)
        self.vis.wait(STEP_DELAY)

        if current == goal:
            self.show(current, path, "solution", "*** GOAL FOUND! ***")
            self.add_log("GOAL STATE REACHED!", GREEN)
            self.vis.wait(DEADEND_DELAY)
            return path

        if depth <= 0:
            self.show(current, path, "deadend", "DEAD END - LIMIT!")
            self.add_log(f"Dead end at depth {len(path)-1} - limit reached", RED)
            self.backtrack_count += 1
            self.vis.wait(DEADEND_DELAY)
            return None

        neighbors = self.get_neighbors(current)
        for i, (neighbor, move) in enumerate(neighbors):
            if neighbor not in [p[0] for p in path]:
                self.add_log(f"Trying move: {move} (option {i+1}/{len(neighbors)})", CYAN)
                result = self.dls(neighbor, goal, depth - 1, path + [(neighbor, move)])
                if result is not None:
                    return result
                self.backtrack_count += 1
                self.show(current, path, "backtrack", f"BACKTRACKING from {move}...")
                self.add_log(f"Backtrack from {move}, trying alternative...", MAGENTA)
                self.vis.wait(BACKTRACK_DELAY)

        self.add_log(f"All moves exhausted at depth {len(path)-1}", RED)
        return None

    def solve_ids(self, max_depth=20):
        """Iterative Deepening Search dengan visualisasi."""
        for limit in range(max_depth):
            self.current_depth_limit = limit
            self.add_log(f"=== Starting depth limit: {limit} ===", CYAN)

            path_moves = ["Start"]
            self.vis.render_frame(self.start, self.goal, "exploring",
                                  f"NEW DEPTH LIMIT: {limit}",
                                  self.get_stats(0), self.log, path_moves)
            self.vis.wait(NEWLIMIT_DELAY)

            result = self.dls(self.start, self.goal, limit,
                              [(self.start, "Start")])
            if result:
                return result, limit

            self.add_log(f"Depth {limit} exhausted, increasing limit...", ORANGE)
        return None, None


def replay_solution(vis, solution, goal):
    """Replay langkah solusi dengan animasi."""
    total = len(solution)
    for i, (state, move) in enumerate(solution):
        vis.handle_events()
        vis.screen.fill(DARK_BG)

        # Header
        pygame.draw.rect(vis.screen, PANEL_BG, (0, 0, WIDTH, 55))
        pygame.draw.line(vis.screen, GREEN, (0, 55), (WIDTH, 55), 2)
        t = vis.font_title.render("SOLUTION REPLAY", True, GREEN)
        vis.screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 16))

        # Grid centered
        gx = WIDTH // 2 - (TILE_SIZE * 3 + GRID_PAD * 4) // 2
        gy = 120
        vis.draw_grid(state, goal, "solution", gx, gy)

        # Step info
        step_t = vis.font_stat_bold.render(f"Step {i} / {total - 1}  —  Move: {move}", True, WHITE)
        vis.screen.blit(step_t, (WIDTH // 2 - step_t.get_width() // 2, 380))

        # Progress bar
        bar_w = 400
        bar_h = 20
        bar_x = WIDTH // 2 - bar_w // 2
        bar_y = 420
        pygame.draw.rect(vis.screen, (30, 30, 40), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        fill_w = int((i / max(total - 1, 1)) * bar_w)
        if fill_w > 0:
            pygame.draw.rect(vis.screen, GREEN, (bar_x, bar_y, fill_w, bar_h), border_radius=6)
        pygame.draw.rect(vis.screen, GRAY, (bar_x, bar_y, bar_w, bar_h), 1, border_radius=6)

        pygame.display.flip()
        vis.wait(SOLUTION_DELAY)


# ==================== MAIN ====================
if __name__ == "__main__":
    vis = PuzzleVisualizer()
    vis.splash_screen(START, GOAL)

    solver = PuzzleSolver(START, GOAL, vis)
    solution, depth_found = solver.solve_ids()

    if solution:
        vis.wait(500)
        replay_solution(vis, solution, GOAL)
        vis.summary_screen(solver.nodes_explored, solver.backtrack_count, len(solution) - 1)
    else:
        # Error screen
        vis.screen.fill(DARK_BG)
        t = vis.font_big.render("NO SOLUTION FOUND", True, RED)
        vis.screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 20))
        pygame.display.flip()
        vis.wait(3000)

    pygame.quit()
