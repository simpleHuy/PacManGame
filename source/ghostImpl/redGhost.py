
import heapq
from ghost import Ghost

class RedGhost(Ghost):
    """
    Red Ghost implementation that uses A* algorithm for pathfinding.
    """
    def __init__(self, position, cell_size, maze, target=None):
        # Call the parent constructor with red color
        super().__init__(position, cell_size, maze, target, color=(255, 0, 0))
        
        # A* specific statistics
        self.expanded_nodes = 0
        self.last_pos = None

    def manhattan_distance(self, start, end):
        """Heuristic function for A* algorithm using Manhattan distance"""
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def calculate_path(self):
        """
        Implement A* pathfinding algorithm to find path to Pacman.
        Overrides the abstract method from Ghost base class.
        """
        if not self.target:
            return []
            
        # Get current grid position of ghost and pacman
        start = self.get_grid_position(self.x, self.y)
        goal = self.get_grid_position(self.target.x, self.target.y)
        
        # Reset statistics for new search
        self.expanded_nodes = 0
        
        # A* algorithm implementation
        open_list = []  # Nodes to check
        closed_list = set()  # Nodes already checked
        
        # Initialize start node
        heapq.heappush(open_list, (0, start))
        
        # Track costs and path
        g_costs = {start: 0}
        came_from = {}
        
        while open_list:
            # Get node with lowest f-score
            _, current = heapq.heappop(open_list)
            self.expanded_nodes += 1
            
            if current == goal:
                # If goal found, reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
                
            closed_list.add(current)
            
            # Check all valid neighbors
            neighbors = self.get_neighbors(current[0], current[1])
            
            for neighbor in neighbors:
                if neighbor in closed_list:
                    continue
                
                # Calculate tentative g score
                tentative_g = g_costs[current] + 1
                
                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    # Found a better path to neighbor
                    came_from[neighbor] = current
                    g_costs[neighbor] = tentative_g
                    f_cost = tentative_g + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor))
        
        # Store explored nodes for visualization
        if self.debug_mode:
            self.explored_nodes = [self.get_pixel_position(x, y) for x, y in closed_list]
            
        return []  # Return empty path if no path found
