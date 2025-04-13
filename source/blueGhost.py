import pygame
from collections import deque

class BlueGhost:
    def __init__(self, x, y, radius, speed, maze, cell_size):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.maze = maze
        self.cell_size = cell_size
        self.color = (0, 0, 255)
        self.path = []
        self.direction = pygame.Vector2(0, 0)

    def get_grid_pos(self):
        return int(self.x // self.cell_size), int(self.y // self.cell_size)

    def bfs(self, start, goal):
        queue = deque()
        visited = set()
        parent = {}

        queue.append(start)
        visited.add(start)

        while queue:
            current = queue.popleft()
            if current == goal:
                break

            x, y = current
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

            for nx, ny in neighbors:
                nx, ny = int(nx), int(ny)
                if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]):
                    if self.maze[ny][nx] != '#' and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))
                        parent[(nx, ny)] = current

        # reconstruct path
        path = []
        node = goal
        while node != start and node in parent:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path

    def update(self, pacman_pos):
        pac_col = int(pacman_pos[0] // self.cell_size)
        pac_row = int(pacman_pos[1] // self.cell_size)
        start = self.get_grid_pos()
        goal = (pac_col, pac_row)
        self.path = self.bfs(start, goal)

        # Đặt hướng di chuyển tiếp theo
        if self.path:
            next_cell = self.path[0]
            dx = next_cell[0] - start[0]
            dy = next_cell[1] - start[1]
            self.direction = pygame.Vector2(dx, dy)

    def move(self):
        # Di chuyển khi ở gần tâm ô
        if abs(self.x % self.cell_size - self.cell_size // 2) < 2 and abs(self.y % self.cell_size - self.cell_size // 2) < 2:
            if self.path:
                next_cell = self.path.pop(0)
                dx = next_cell[0] - int(self.x // self.cell_size)
                dy = next_cell[1] - int(self.y // self.cell_size)
                self.direction = pygame.Vector2(dx, dy)

        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self, screen):
        # Vẽ ghost
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # Vẽ đường đi nét đứt mảnh
        if len(self.path) > 0:
            points = []
            for col, row in self.path:
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2
                points.append((x, y))

            # Thêm vị trí hiện tại của ghost vào đầu
            points.insert(0, (int(self.x), int(self.y)))

            # Vẽ các chấm nhỏ như nét đứt
            for i in range(len(points) - 1):
                start = points[i]
                end = points[i + 1]

                steps = 5  # số bước càng cao, khoảng cách chấm càng ngắn
                for j in range(0, steps):
                    t = j / steps
                    dot_x = int(start[0] + t * (end[0] - start[0]))
                    dot_y = int(start[1] + t * (end[1] - start[1]))
                    if j % 2 == 0:
                        pygame.draw.circle(screen, (100, 255, 255), (dot_x, dot_y), 1)  # nhỏ và mảnh


