from ghost import Ghost

class DFSFollowingGhost(Ghost):
    def __init__(self, position, cell_size, maze, target_ghost=None, color=(100, 200, 100)):
        """
        Initialize a ghost that uses Depth-First Search to follow another ghost
        
        :param position: Initial pixel position (x, y)
        :param cell_size: Size of each cell in the maze
        :param maze: Maze object for collision detection
        :param target_ghost: The ghost that this ghost will follow
        :param color: Color of the ghost (default is a green shade)
        """
        super().__init__(position, cell_size, maze, target=target_ghost, color=color)
        
        # Tracking exploration for DFS
        self.explored_nodes = []
    
    def calculate_path(self):
        """
        Calculate path using Depth-First Search to follow the target ghost
        
        :return: List of grid coordinates representing the path
        """
        # If no target ghost, return empty path
        if not self.target:
            return []
        
        # Get current grid positions
        start_grid_x, start_grid_y = self.get_grid_position(self.x, self.y)
        target_grid_x, target_grid_y = self.get_grid_position(self.target.x, self.target.y)
        
        # Reset explored nodes for debug visualization
        self.explored_nodes = []
        
        # Initialize DFS variables
        stack = [(start_grid_x, start_grid_y, [])]
        visited = set([(start_grid_x, start_grid_y)])
        
        # Main DFS loop
        while stack:
            current_x, current_y, path = stack.pop()
            
            # If reached the target, return the path
            if current_x == target_grid_x and current_y == target_grid_y:
                return path + [(current_x, current_y)]
            
            # Add to explored nodes for debug visualization
            pixel_pos = self.get_pixel_position(current_x, current_y)
            self.explored_nodes.append(pixel_pos)
            
            # Get valid neighboring cells
            neighbors = self.get_neighbors(current_x, current_y)
            
            # Add unvisited neighbors to stack
            for nx, ny in neighbors:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append((nx, ny, path + [(current_x, current_y)]))
        
        # No path found
        return []