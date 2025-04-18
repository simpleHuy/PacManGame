from collections import deque
import pygame

class DFSGhost:
    def __init__(self, x, y, radius, speed, maze, cell_size, target=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.maze = maze
        self.cell_size = cell_size
        self.target = target  # Pacman as the target
        self.color = (255, 105, 180)  # Pink color for the ghost
        self.path = []
        self.direction = pygame.Vector2(0, 0)

        # Initialize attributes to track statistics
        self.search_time = 0
        self.expanded_nodes = 0  # Initialize expanded_nodes variable
        self.memory_usage = 0

    def get_grid_pos(self):
        return int(self.x // self.cell_size), int(self.y // self.cell_size)

    # Find the path using DFS algorithm
    def dfs(self, start, goal):
        stack = [(start, [])]  # Stack to store cells to check
        visited = set()  # Set to track visited cells

        while stack:
            current, path = stack.pop()  # Get the last element from the stack
            x, y = current
            if current == goal:  # If the current cell is the goal, stop
                return path + [current]

            if current not in visited:
                visited.add(current)  # Mark as visited
                neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]  # Neighbors (right, left, up, down)

                # Check each neighboring cell
                for nx, ny in neighbors:
                    if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]):  # Check if the cell is valid
                        if self.maze[ny][nx] != '#' and (nx, ny) not in visited:
                            stack.append(((nx, ny), path + [current]))  # Add to stack

        return []  # If no path found

    def update(self, pacman):
        # Access Pacman's x and y directly
        pac_col = int(pacman.x // self.cell_size)
        pac_row = int(pacman.y // self.cell_size)
        start = self.get_grid_pos()
        goal = (pac_col, pac_row)
        self.path = self.dfs(start, goal)

        # Set the next direction to move
        if self.path:
            next_cell = self.path[0]
            dx = next_cell[0] - start[0]
            dy = next_cell[1] - start[1]
            self.direction = pygame.Vector2(dx, dy)

    def move(self):
        # Move when close to the center of the cell
        if abs(self.x % self.cell_size - self.cell_size // 2) < 2 and abs(self.y % self.cell_size - self.cell_size // 2) < 2:
            if self.path:
                next_cell = self.path.pop(0)
                dx = next_cell[0] - int(self.x // self.cell_size)
                dy = next_cell[1] - int(self.y // self.cell_size)
                self.direction = pygame.Vector2(dx, dy)

        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

    def draw(self, screen):
        # Draw the ghost
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # Draw the path as dashed lines
        if len(self.path) > 0:
            points = []
            for col, row in self.path:
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2
                points.append((x, y))

            points.insert(0, (int(self.x), int(self.y)))

            # Draw the path as dashes
            for i in range(len(points) - 1):
                start = points[i]
                end = points[i + 1]

                steps = 5  # The higher the number of steps, the smaller the dashes
                for j in range(0, steps):
                    t = j / steps
                    dot_x = int(start[0] + t * (end[0] - start[0]))
                    dot_y = int(start[1] + t * (end[1] - start[1]))
                    if j % 2 == 0:
                        pygame.draw.circle(screen, (100, 255, 255), (dot_x, dot_y), 1)  # Small and thin
