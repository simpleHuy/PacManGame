from ghost import Ghost

class PinkGhost(Ghost):
    def __init__(self, position, cell_size, maze, target_ghost=None):
        super().__init__(position, cell_size, maze, target=target_ghost, ghostType='pink')
        
    
    def calculate_path(self):
        """
        Implement Depth-First Search pathfinding algorithm to find path to Pacman.
        """
        if not self.target:
            return []
        
        # Get current grid position of ghost and Pacman
        start = self.get_grid_position(self.x, self.y)
        goal = self.get_grid_position(self.target.x, self.target.y)
        
        # Reset explored nodes
        self.explored_nodes = []
        
        # DFS algorithm implementation
        stack = [(start, [])]
        visited = set([start])

        while stack:
            current, path = stack.pop()
            
            # Reached the goal
            if current == goal:
                return path + [current]
            
            # Add to explored nodes for visualization
            pixel_pos = self.get_pixel_position(current[0], current[1])
            self.explored_nodes.append(pixel_pos)
            
            # Get valid neighbors
            neighbors = self.get_neighbors(current[0], current[1])
            
            # Explore neighbors in a depth-first manner
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Track the full path to this neighbor
                    new_path = path + [current]
                    stack.append((neighbor, new_path))
        
        # If no path found, return to start
        return [start]

