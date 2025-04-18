import pygame
import math
from abc import ABC, abstractmethod

class Ghost(pygame.sprite.Sprite, ABC):
    """
    Base class for all ghosts with common properties and behaviors.
    Can be extended with different pathfinding algorithms.
    Now inherits from pygame.sprite.Sprite for better game integration.
    """
    all_ghosts = pygame.sprite.Group()

    def __init__(self, position, cell_size, maze, target=None, color=(255, 255, 255)):
            pygame.sprite.Sprite.__init__(self)
            self.x, self.y = position
            self.cell_size = cell_size
            
            # Replace radius with width and height
            self.width = cell_size  # Full cell width
            self.height = cell_size  # Full cell height
            
            self.speed = 1  # Movement speed
            self.maze = maze
            self.target = target  # This will be the Pacman object
            self.color = color
            
            # Create image and rect attributes (required for pygame.sprite.Sprite)
            self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            
            # Path variables
            self.current_path = []
            self.path_update_timer = 0
            self.path_update_delay = 30  # Update path every 30 frames (0.5 seconds at 60FPS)
            
            # Visualization variables for debug
            self.explored_nodes = []
            self.debug_mode = False
            
            # Add to sprite group
            Ghost.all_ghosts.add(self)    

    def kill(self):
        """Override the sprite kill method to remove from all_ghosts"""
        pygame.sprite.Sprite.kill(self)

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
        """
        Get valid neighboring cells 
        - Exclude maze walls
        - Exclude cells occupied by other ghosts
        """
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        neighbors = []
        
        # Get all grid positions of other ghosts
        ghost_positions = set()
        for ghost in Ghost.all_ghosts:
            if ghost != self:
                grid_pos = self.get_grid_position(ghost.x, ghost.y)
                ghost_positions.add(grid_pos)
        
        for dx, dy in directions:
            new_x, new_y = grid_x + dx, grid_y + dy
            
            # Check if this cell is not occupied by another ghost
            if (new_x, new_y) not in ghost_positions:
                # Create a temporary rect to check collision with walls
                temp_pixel_x, temp_pixel_y = self.get_pixel_position(new_x, new_y)
                temp_rect = pygame.Rect(
                    temp_pixel_x - self.width // 2, 
                    temp_pixel_y - self.height // 2,
                    self.width, 
                    self.height
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
        """Update ghost position and path - now matches the sprite update pattern"""
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
            self.rect.center = (self.x, self.y)
            
            # If we've reached the next position, remove it from the path
            if abs(self.x - next_pixel_x) < self.speed and abs(self.y - next_pixel_y) < self.speed:
                self.current_path.pop(0)

        # Check collision with other ghosts
        for ghost in Ghost.all_ghosts:
            if ghost != self and self.check_collision_with_ghost(ghost):
                self.avoid_collision()
                break
                
        # Redraw the ghost onto its image surface
        self._draw_ghost_image()
    
    def _draw_ghost_image(self):
        """Draw the ghost as a rectangular shape"""
        # Clear the surface with transparent background
        self.image.fill((0, 0, 0, 0))
        
        # Draw the rectangle body
        rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.image, self.color, rect)
        
        # Draw eyes (proportional to rectangle size)
        eye_width = self.width // 4
        eye_height = self.height // 4
        
        # Left eye
        left_eye_rect = pygame.Rect(
            self.width // 4 - eye_width // 2, 
            self.height // 3, 
            eye_width, 
            eye_height
        )
        pygame.draw.rect(self.image, (255, 255, 255), left_eye_rect)
        
        # Right eye
        right_eye_rect = pygame.Rect(
            3 * self.width // 4 - eye_width // 2, 
            self.height // 3, 
            eye_width, 
            eye_height
        )
        pygame.draw.rect(self.image, (255, 255, 255), right_eye_rect)

    def draw_debug(self, screen):
        """Draw debug information on the screen"""
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
        """
        Returns a list of grid cells occupied by other ghosts
        Ensures the current ghost doesn't count its own cell
        """
        occupied_cells = []
        for ghost in Ghost.all_ghosts:
            if ghost != self:  # Don't include self
                grid_x, grid_y = self.get_grid_position(ghost.x, ghost.y)
                occupied_cells.append((grid_x, grid_y))
        return occupied_cells
    
    def avoid_collision(self):
        """
        Enhanced collision avoidance strategy to separate overlapping ghosts
        """
        # Find all ghosts this ghost is colliding with
        colliding_ghosts = [
            ghost for ghost in Ghost.all_ghosts 
            if ghost != self and self.check_collision_with_ghost(ghost)
        ]
        
        if not colliding_ghosts:
            return
        
        # Aggressive separation strategy
        for other_ghost in colliding_ghosts:
            # Calculate overlap direction
            dx = self.x - other_ghost.x
            dy = self.y - other_ghost.y
            
            # Normalize direction
            distance = math.sqrt(dx**2 + dy**2)
            if distance == 0:
                # If exactly on top of each other, add small random offset
                import random
                dx = random.choice([-1, 1]) * self.width
                dy = random.choice([-1, 1]) * self.height
                distance = math.sqrt(dx**2 + dy**2)
            
            # Separate ghosts by moving them apart
            # Multiply speed to ensure separation
            separation_factor = max(self.width, self.height)
            move_x = (dx / distance) * separation_factor
            move_y = (dy / distance) * separation_factor
            
            # Apply movement
            self.x += move_x
            self.y += move_y
            
            # Update rect
            self.rect.center = (self.x, self.y)
        
        # Force path recalculation
        self.current_path = self.calculate_path()
        self.path_update_timer = self.path_update_delay

    def check_collision_with_ghost(self, other_ghost):
        """
        More robust collision detection for rectangular ghosts
        """
        # Calculate the overlap between two rectangles
        x_overlap = (abs(self.x - other_ghost.x) * 2 < (self.width + other_ghost.width))
        y_overlap = (abs(self.y - other_ghost.y) * 2 < (self.height + other_ghost.height))
        
        return x_overlap and y_overlap  

    @classmethod
    def update_all(cls):
        """Update all ghosts in the group"""
        cls.all_ghosts.update()
        
    @classmethod
    def draw_all(cls, screen):
        """Draw all ghosts in the group"""
        cls.all_ghosts.draw(screen)
        
        # Draw debug info for each ghost
        for ghost in cls.all_ghosts:
            if ghost.debug_mode:
                ghost.draw_debug(screen)