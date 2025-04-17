from collections import deque
import pygame

class BlueGhost:
    # Initialize the ghost's attributes
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

        # Initialize new attributes to track statistics
        self.search_time = 0
        self.expanded_nodes = 0  # Initialize expanded_nodes variable
        self.memory_usage = 0

    def get_grid_pos(self):
        return int(self.x // self.cell_size), int(self.y // self.cell_size)

    # Find the path using BFS algorithm
    def bfs(self, start, goal):
        # Initialize data structures for BFS
        queue = deque()  # Queue to store the cells to check
        visited = set()  # Set of visited cells
        parent = {}  # Dictionary to store parent cells, to reconstruct the path

        queue.append(start)  # Start from the start cell
        visited.add(start)  # Mark the start cell as visited

        while queue:  # While the queue is not empty
            current = queue.popleft()  # Get the first cell from the queue
            self.expanded_nodes += 1  # Increment the number of expanded nodes

            if current == goal:  # If the current cell is the goal, stop
                break

            x, y = current  # Get the (x, y) coordinates of the current cell
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]  # Neighboring cells (right, left, up, down)

            # Check each neighboring cell
            for nx, ny in neighbors:
                nx, ny = int(nx), int(ny)  # Round the coordinates
                if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]):  # Check if the cell is valid (within the maze)
                    if self.maze[ny][nx] != '#' and (nx, ny) not in visited:  # Valid if not a wall (#) and not visited
                        queue.append((nx, ny))  # Add the cell to the queue
                        visited.add((nx, ny))  # Mark the cell as visited
                        parent[(nx, ny)] = current  # Store the parent of this cell

        # Reconstruct the path from the goal to the start
        path = []  # List to store the path
        node = goal  # Start from the goal
        while node != start and node in parent:  # Move back from the goal to the start
            path.append(node)  # Add the cell to the path
            node = parent[node]  # Get the parent of the current cell
        path.reverse()  # Reverse the path to go from start to goal
        return path

    def update(self, pacman_pos):
        pac_col = int(pacman_pos[0] // self.cell_size)
        pac_row = int(pacman_pos[1] // self.cell_size)
        start = self.get_grid_pos()
        goal = (pac_col, pac_row)
        self.path = self.bfs(start, goal)

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

            # Add the current position of the ghost at the beginning
            points.insert(0, (int(self.x), int(self.y)))

            # Draw the dots as dashes
            for i in range(len(points) - 1):
                start = points[i]
                end = points[i + 1]

                steps = 5  # The higher the number of steps, the smaller the dots
                for j in range(0, steps):
                    t = j / steps
                    dot_x = int(start[0] + t * (end[0] - start[0]))
                    dot_y = int(start[1] + t * (end[1] - start[1]))
                    if j % 2 == 0:
                        pygame.draw.circle(screen, (100, 255, 255), (dot_x, dot_y), 1)  # Small and thin
