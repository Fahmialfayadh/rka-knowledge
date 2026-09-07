
"""
Kingdom War Simulation - Pathfinding
Grid Map dan A* pathfinding algorithm.
"""

from __future__ import annotations

import heapq
from typing import List, Tuple

from .utils import clamp


class GridMap:
    def __init__(self, x: float, y: float, w: float, h: float, cell_size: int = 20):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.cell_size = cell_size
        self.cols = int(w // cell_size)
        self.rows = int(h // cell_size)
        # Terrain codes: 0 = Grass, 1 = Wall, 2 = Rock, 3 = River, 4 = Forest, 5 = Road
        self.cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def world_to_grid(self, wx: float, wy: float) -> Tuple[int, int]:
        c = int((wx - self.x) // self.cell_size)
        r = int((wy - self.y) // self.cell_size)
        return clamp(c, 0, self.cols - 1), clamp(r, 0, self.rows - 1)

    def grid_to_world(self, c: int, r: int) -> Tuple[float, float]:
        wx = self.x + c * self.cell_size + self.cell_size / 2.0
        wy = self.y + r * self.cell_size + self.cell_size / 2.0
        return wx, wy

    def is_walkable(self, c: int, r: int) -> bool:
        if not (0 <= c < self.cols and 0 <= r < self.rows):
            return False
        return self.cells[r][c] not in (1, 2, 3)  # Wall, Rock, River are fully blocked

    def get_cost(self, c: int, r: int) -> float:
        if not (0 <= c < self.cols and 0 <= r < self.rows):
            return float('inf')
        code = self.cells[r][c]
        # Costs: grass=1.0, wall=inf, rock=inf, river=inf, forest=3.0, road=0.5
        weights = {0: 1.0, 1: float('inf'), 2: float('inf'), 3: float('inf'), 4: 3.0, 5: 0.5}
        return weights.get(code, 1.0)


class AStar:
    @staticmethod
    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def find_nearest_walkable(grid_map: GridMap, center: Tuple[int, int]) -> Tuple[int, int]:
        if grid_map.is_walkable(center[0], center[1]):
            return center
        # BFS search outward for closest walkable cell
        queue = [center]
        visited = {center}
        while queue:
            curr = queue.pop(0)
            c, r = curr
            if grid_map.is_walkable(c, r):
                return (c, r)
            for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nbr = (c + dc, r + dr)
                if 0 <= nbr[0] < grid_map.cols and 0 <= nbr[1] < grid_map.rows:
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append(nbr)
        return center # fallback

    @staticmethod
    def find_path(grid_map: GridMap, start: Tuple[int, int], target: Tuple[int, int]) -> List[Tuple[int, int]]:
        start = AStar.find_nearest_walkable(grid_map, start)
        target = AStar.find_nearest_walkable(grid_map, target)

        if start == target:
            return [start]

        open_set = []
        heapq.heappush(open_set, (0.0, start))
        came_from = {}
        g_score = {start: 0.0}
        f_score = {start: AStar.heuristic(start, target)}
        closed_set = set()

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            closed_set.add(current)
            c, r = current

            for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nbr = (c + dc, r + dr)
                if not grid_map.is_walkable(nbr[0], nbr[1]) or nbr in closed_set:
                    continue

                cost = grid_map.get_cost(nbr[0], nbr[1])
                tentative_g = g_score[current] + cost

                if nbr not in g_score or tentative_g < g_score[nbr]:
                    came_from[nbr] = current
                    g_score[nbr] = tentative_g
                    f_score[nbr] = tentative_g + AStar.heuristic(nbr, target)
                    heapq.heappush(open_set, (f_score[nbr], nbr))

        return [] # empty path if unreachable
