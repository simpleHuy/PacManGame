import pygame
import math
from abc import ABC, abstractmethod

class Ghost(ABC):
    """
    Base class for all ghosts with common properties and behaviors.
    Can be extended with different pathfinding algorithms.
    """
    all_ghosts = []
    

    def __init__(self, position, cell_size, maze, target=None, color=(255, 255, 255)):
        self.x, self.y = position
        self.cell_size = cell_size
        self.radius = int(cell_size * 0.5)
        self.speed = 1 #max(1, int(cell_size / 12))
        self.maze = maze
        self.target = target  # This will be the Pacman object
        self.color = color
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                              self.radius * 2, self.radius * 2)
        
        # Path variables
        self.current_path = []
        self.path_update_timer = 0
        self.path_update_delay = 30  # Update path every 30 frames (0.5 seconds at 60FPS)
        
        # Visualization variables for debug
        self.explored_nodes = []
        self.debug_mode = False
        Ghost.all_ghosts.append(self)

    def __del__(self):
        """Remove self from all_ghosts when deleted"""
        if self in Ghost.all_ghosts:
            Ghost.all_ghosts.remove(self)

    def set_target(self, target):
        """Set the target (usually Pacman) for the ghost to chase"""
        self.target = target

    def get_grid_position(self, x, y):
        """Convert pixel coordinates to grid coordinates"""
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        return grid_x, grid_y

    def get_pixel_position(self, grid_x, grid_y):
        """Convert grid coordinates to pixel coordinates (center of cell)"""
        pixel_x = grid_x * self.cell_size + self.cell_size // 2
        pixel_y = grid_y * self.cell_size + self.cell_size // 2
        return pixel_x, pixel_y

    def get_neighbors(self, grid_x, grid_y):
        """Get valid neighboring cells (not walls)"""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        neighbors = []
        
        for dx, dy in directions:
            new_x, new_y = grid_x + dx, grid_y + dy
            
            # Create a temporary rect to check collision with walls
            temp_pixel_x, temp_pixel_y = self.get_pixel_position(new_x, new_y)
            temp_rect = pygame.Rect(
                temp_pixel_x - self.radius, temp_pixel_y - self.radius,
                self.radius * 2, self.radius * 2
            )
            
            # Check if this position would collide with a wall
            if not self.maze.check_collision(temp_rect):
                neighbors.append((new_x, new_y))
                
        return neighbors

    @abstractmethod
    def calculate_path(self):
        """
        Abstract method to be implemented by subclasses.
        Should calculate a path to the target using a specific algorithm.
        """
        pass

    def update(self):
        """Update ghost position and path"""
        # Update path periodically
        self.path_update_timer += 1
        if self.path_update_timer >= self.path_update_delay:
            self.current_path = self.calculate_path()
            self.path_update_timer = 0
        
        # If we have a path, follow it
        if self.current_path and len(self.current_path) > 1:
            # Get next position in path (skip current position)
            next_grid_x, next_grid_y = self.current_path[1]
            next_pixel_x, next_pixel_y = self.get_pixel_position(next_grid_x, next_grid_y)
            
            # Calculate direction to next position
            dx = next_pixel_x - self.x
            dy = next_pixel_y - self.y
            
            # Normalize direction
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                dx = dx / distance * min(self.speed, distance)
                dy = dy / distance * min(self.speed, distance)
            
            # Move ghost
            self.x += dx
            self.y += dy
            
            # Update rect
            self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                  self.radius * 2, self.radius * 2)
            
            # If we've reached the next position, remove it from the path
            if abs(self.x - next_pixel_x) < self.speed and abs(self.y - next_pixel_y) < self.speed:
                self.current_path.pop(0)

        for ghost in Ghost.all_ghosts:
            if ghost != self and self.check_collision_with_ghost(ghost):
                self.avoid_collision()
                break

    def draw(self, screen):
        """Draw the ghost"""
        # Draw ghost body (semicircle with a wavy bottom)
        ghost_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                              self.radius * 2, self.radius * 2)
        
        # Draw ghost body
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.rect(screen, self.color, (self.x - self.radius, self.y, self.radius * 2, self.radius))
        
        # Draw wavy bottom
        wave_height = max(2, self.radius // 4)
        wave_width = self.radius // 2
        num_waves = 4
        
        for i in range(num_waves):
            wave_x = self.x - self.radius + i * wave_width
            
            # Draw the wavy bottom using a small rectangle
            wave_rect = pygame.Rect(wave_x, self.y + self.radius - wave_height,
                                 wave_width, wave_height * 2)
            if i % 2 == 0:  # Alternating pattern
                pygame.draw.rect(screen, self.color, wave_rect)
            else:
                pygame.draw.rect(screen, (0, 0, 0), wave_rect)
                
        # Draw eyes
        eye_radius = max(2, self.radius // 5)
        left_eye_pos = (self.x - self.radius // 2, self.y - self.radius // 4)
        right_eye_pos = (self.x + self.radius // 2, self.y - self.radius // 4)
        
        pygame.draw.circle(screen, (255, 255, 255), left_eye_pos, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), right_eye_pos, eye_radius)
        
        # Draw pupils - look toward Pacman if it exists
        pupil_radius = max(1, eye_radius // 2)
        
        if self.target:
            # Calculate direction to Pacman
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            
            # Normalize and limit pupil movement
            max_offset = eye_radius - pupil_radius
            if dx != 0 or dy != 0:
                distance = math.sqrt(dx**2 + dy**2)
                dx = dx / distance * min(max_offset, distance)
                dy = dy / distance * min(max_offset, distance)
            
            left_pupil_pos = (left_eye_pos[0] + int(dx//2), left_eye_pos[1] + int(dy//2))
            right_pupil_pos = (right_eye_pos[0] + int(dx//2), right_eye_pos[1] + int(dy//2))
        else:
            left_pupil_pos = left_eye_pos
            right_pupil_pos = right_eye_pos
        
        pygame.draw.circle(screen, (0, 0, 255), left_pupil_pos, pupil_radius)
        pygame.draw.circle(screen, (0, 0, 255), right_pupil_pos, pupil_radius)
        
        # Debug visualization
        if self.debug_mode:
            # Draw explored nodes
            for node in self.explored_nodes:
                pygame.draw.circle(screen, (100, 100, 100), node, 2)
                
            # Draw path
            if len(self.current_path) > 1:
                for i in range(len(self.current_path) - 1):
                    start_grid = self.current_path[i]
                    end_grid = self.current_path[i + 1]
                    
                    start_pixel = self.get_pixel_position(start_grid[0], start_grid[1])
                    end_pixel = self.get_pixel_position(end_grid[0], end_grid[1])
                    
                    pygame.draw.line(screen, self.color, start_pixel, end_pixel, 2)

    def toggle_debug(self):
        """Toggle debug visualization"""
        self.debug_mode = not self.debug_mode

    def check_collision_with_pacman(self):
        """Check if ghost collides with Pacman"""
        if self.target and self.rect.colliderect(self.target.rect):
            return True
        return False
    
    def get_occupied_cells(self):
        """Returns a list of grid cells occupied by other ghosts"""
        occupied_cells = []
        for ghost in Ghost.all_ghosts:
            if ghost != self:  # Don't include self
                grid_x, grid_y = self.get_grid_position(ghost.x, ghost.y)
                occupied_cells.append((grid_x, grid_y))
        return occupied_cells
        
    def check_collision_with_ghost(self, other_ghost):
        """Check if this ghost collides with another ghost"""
        distance = math.sqrt((self.x - other_ghost.x)**2 + (self.y - other_ghost.y)**2)
        collision_threshold = self.radius + other_ghost.radius - 2  # Slightly smaller than sum of radii
        return distance < collision_threshold
    
    def avoid_collision(self):
        """Adjust position to avoid collision with another ghost"""
        # Find all ghosts this ghost is colliding with
        colliding_ghosts = []
        for ghost in Ghost.all_ghosts:
            if ghost != self and self.check_collision_with_ghost(ghost):
                colliding_ghosts.append(ghost)
        
        if not colliding_ghosts:
            return
        
        # Calculate average direction away from colliding ghosts
        dx, dy = 0, 0
        for ghost in colliding_ghosts:
            # Direction from other ghost to this ghost
            direction_x = self.x - ghost.x
            direction_y = self.y - ghost.y
            
            # Normalize
            distance = math.sqrt(direction_x**2 + direction_y**2)
            if distance > 0:
                dx += direction_x / distance
                dy += direction_y / distance
        
        # Normalize the average direction
        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude > 0:
            dx = dx / magnitude
            dy = dy / magnitude
            
        # Move slightly in that direction
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Update rect
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                            self.radius * 2, self.radius * 2)
        
        # Force path recalculation
        self.path_update_timer = self.path_update_delay

