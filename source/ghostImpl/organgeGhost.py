import heapq
import pygame
from ghost import Ghost

class OrangeGhost(Ghost):
    """Ghost that uses Uniform Cost Search algorithm to find Pacman"""
    
    def __init__(self, position, cell_size, maze, target=None):
        # Initialize with orange color
        super().__init__(position, cell_size, maze, target, color=(255, 165, 0))

    def calculate_path(self):
        """Use Uniform Cost Search to find path to Pacman"""
        if not self.target:
            return []
        
        # Get grid positions
        start_grid_x, start_grid_y = self.get_grid_position(self.x, self.y)
        target_grid_x, target_grid_y = self.get_grid_position(self.target.x, self.target.y)
        
        # Priority queue for UCS: (cost, position, path)
        frontier = [(0, (start_grid_x, start_grid_y), [])]
        heapq.heapify(frontier)
        
        # Track visited nodes and their costs
        visited = {}  # {position: cost}
        
        self.explored_nodes = []  # Reset explored nodes for visualization
        
        while frontier:
            cost, current, path = heapq.heappop(frontier)
            current_x, current_y = current
            
            # Add to explored nodes for visualization
            if self.debug_mode:
                pixel_x, pixel_y = self.get_pixel_position(current_x, current_y)
                self.explored_nodes.append((pixel_x, pixel_y))
            
            # Check if we've reached the target
            if (current_x, current_y) == (target_grid_x, target_grid_y):
                return path + [(current_x, current_y)]
            
            # Skip if we've already found a cheaper path to this position
            if (current_x, current_y) in visited and visited[(current_x, current_y)] <= cost:
                continue
                
            # Mark as visited with current cost
            visited[(current_x, current_y)] = cost
            
            # Check all neighbors
            for neighbor in self.get_neighbors(current_x, current_y):
                new_x, new_y = neighbor
                
                # In UCS, all moves have equal cost (1)
                new_cost = cost + 1
                
                # Add to frontier if unvisited or found a cheaper path
                if neighbor not in visited or new_cost < visited[neighbor]:
                    heapq.heappush(frontier, (new_cost, neighbor, path + [(current_x, current_y)]))
        
        # No path found
        return []