
import heapq
from ghost import Ghost

class RedGhost(Ghost):
    """
    Red Ghost implementation that uses A* algorithm for pathfinding.
    """
    def __init__(self, position, cell_size, maze, target=None):
        # Call the parent constructor with red color
        super().__init__(position, cell_size, maze, target, ghostType='red')
        
        # A* specific statistics
        self.expanded_nodes = 0
        self.last_pos = None

    def manhattan_distance(self, start, end):
        """Heuristic function for A* algorithm using Manhattan distance"""
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def calculate_path(self):
        """Use A* Search to find path to Pacman"""
        if not self.target:
            return []
        
        # Get grid positions
        start = self.get_grid_position(self.x, self.y)
        goal = self.get_grid_position(self.target.x, self.target.y)
        
        # Priority queue for A*: (f_cost, g_cost, position, path)
        frontier = [(self.manhattan_distance(start, goal), 0, start, [])]
        heapq.heapify(frontier)
        
        # Track visited nodes and their g_costs
        visited = {}  # {position: g_cost}
        
        self.explored_nodes = []  # Reset for visualization
        
        while frontier:
            f_cost, g_cost, current, path = heapq.heappop(frontier)
            current_x, current_y = current
            
            # Add to explored nodes for visualization
            if self.debug_mode:
                pixel_x, pixel_y = self.get_pixel_position(current_x, current_y)
                self.explored_nodes.append((pixel_x, pixel_y))
            
            # Reached the goal
            if current == goal:
                self.current_path = path + [current]
                return self.current_path
            
            # Skip if we’ve already visited with a cheaper cost
            if current in visited and visited[current] <= g_cost:
                continue
            
            visited[current] = g_cost
            
            for neighbor in self.get_neighbors(current_x, current_y):
                new_g = g_cost + 1
                if neighbor not in visited or new_g < visited[neighbor]:
                    h = self.manhattan_distance(neighbor, goal)
                    new_f = new_g + h
                    heapq.heappush(frontier, (new_f, new_g, neighbor, path + [current]))
        
        # No path found
        self.current_path = []
        return []
