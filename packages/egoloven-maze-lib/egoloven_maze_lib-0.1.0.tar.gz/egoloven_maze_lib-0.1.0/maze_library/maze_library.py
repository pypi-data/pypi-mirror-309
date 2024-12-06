import random
import heapq
import json
from typing import List, Tuple, Dict


class MazeGenerator:
    @staticmethod
    def generate_maze(width: int, height: int, seed: int = None) -> List[List[int]]:
        if seed is not None:
            random.seed(seed)

        maze = [[1] * width for _ in range(height)]

        def carve_passages(x: int, y: int):
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < height and 0 < ny < width and maze[nx][ny] == 1:
                    maze[nx][ny] = 0
                    maze[x + dx // 2][y + dy // 2] = 0
                    carve_passages(nx, ny)

        maze[1][1] = 0
        carve_passages(1, 1)
        return maze


class Pathfinder:
    @staticmethod
    def dijkstra(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        rows, cols = len(maze), len(maze[0])
        dist = {start: 0}
        prev = {start: None}
        pq = [(0, start)]

        while pq:
            current_dist, current = heapq.heappop(pq)
            if current == end:
                break

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                    new_dist = current_dist + 1
                    if (nx, ny) not in dist or new_dist < dist[(nx, ny)]:
                        dist[(nx, ny)] = new_dist
                        prev[(nx, ny)] = current
                        heapq.heappush(pq, (new_dist, (nx, ny)))

        path = []
        while end:
            path.append(end)
            end = prev.get(end)
        return path[::-1]

    @staticmethod
    def a_star(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        rows, cols = len(maze), len(maze[0])
        open_set = [(0 + heuristic(start, end), 0, start)]
        came_from = {start: None}
        g_score = {start: 0}

        while open_set:
            _, current_g, current = heapq.heappop(open_set)
            if current == end:
                break

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                    tentative_g = current_g + 1
                    if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                        g_score[(nx, ny)] = tentative_g
                        priority = tentative_g + heuristic((nx, ny), end)
                        heapq.heappush(open_set, (priority, tentative_g, (nx, ny)))
                        came_from[(nx, ny)] = current

        path = []
        while end:
            path.append(end)
            end = came_from.get(end)
        return path[::-1]

    @staticmethod
    def dfs(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        stack = [start]
        visited = set()
        parent = {start: None}

        while stack:
            current = stack.pop()
            if current in visited:
                continue

            visited.add(current)
            if current == end:
                break

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                    stack.append((nx, ny))
                    parent[(nx, ny)] = current

        path = []
        while end:
            path.append(end)
            end = parent.get(end)
        return path[::-1]


class FileHandler:
    @staticmethod
    def save_maze(maze: List[List[int]], filename: str):
        with open(filename, 'w') as f:
            json.dump(maze, f)

    @staticmethod
    def load_maze(filename: str) -> List[List[int]]:
        with open(filename, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_path(path: List[Tuple[int, int]], filename: str):
        with open(filename, 'w') as f:
            json.dump(path, f)

    @staticmethod
    def load_path(filename: str) -> List[Tuple[int, int]]:
        with open(filename, 'r') as f:
            return json.load(f)

