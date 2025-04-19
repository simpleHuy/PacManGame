from collections import deque
from ghost import Ghost

class BlueGhost(Ghost):
    """
    Blue Ghost implementation that uses BFS algorithm for pathfinding.
    """
    def __init__(self, position, cell_size, maze, target=None):
        # Call the parent constructor with blue color
        super().__init__(position, cell_size, maze, target, ghostType='blue')
        
        # BFS specific statistics
        self.expanded_nodes = 0
        self.search_time = 0
        self.memory_usage = 0

    def calculate_path(self):
        """
        Implement BFS pathfinding algorithm to find path to Pacman.
        Overrides the abstract method from Ghost base class.
        """
        if not self.target:
            return []
            
        # Get current grid position of ghost and pacman
        start = self.get_grid_position(self.x, self.y)
        goal = self.get_grid_position(self.target.x, self.target.y)
        
        # Reset statistics for new search
        self.expanded_nodes = 0
        
        # BFS algorithm implementation
        queue = deque()
        visited = set()
        parent = {}

        queue.append(start)
        visited.add(start)

        while queue:
            current = queue.popleft()
            self.expanded_nodes += 1

            if current == goal:
                break

            # Get valid neighbors
            neighbors = self.get_neighbors(current[0], current[1])

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current

        # Store explored nodes for visualization
        if self.debug_mode:
            self.explored_nodes = [self.get_pixel_position(x, y) for x, y in visited]

        # Reconstruct path
        path = []
        node = goal
        
        while node != start and node in parent:
            path.append(node)
            node = parent[node]
            
        path.append(start)
        path.reverse()
        
        return path