import pygame
import math

class Pacman(pygame.sprite.Sprite):
    def __init__(self, position, cell_size, maze):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.radius = int(cell_size * 0.5)
        self.cell_size = cell_size
        # Scale speed relative to cell size
        self.speed = max(1, int(cell_size / 8))
        self.direction = 'right'  # Initial direction
        self.next_direction = None
        self.animation_count = 0
        self.open_close = 0  # Animation state (0: closed, 1: half open, 2: fully open)
        
        # Create image and rect attributes (required for pygame.sprite.Sprite)
        self.image = pygame.Surface([self.radius * 2, self.radius * 2], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.frozen = True  # Pacman starts frozen
        self.maze = maze  # Store maze reference for collision detection
        
        # First draw of the sprite image
        self._draw_pacman_image()
    
    def change_direction(self, new_direction):
        # Store next direction, will change when possible
        self.next_direction = new_direction
    
    def update(self):
        """Update method required by pygame.sprite.Sprite"""
        if self.frozen:
            return
            
        # Try to change to the queued direction if possible
        if self.next_direction:
            temp_x, temp_y = self.x, self.y
            
            if self.next_direction == 'up':
                temp_y -= self.speed
            elif self.next_direction == 'down':
                temp_y += self.speed
            elif self.next_direction == 'left':
                temp_x -= self.speed
            elif self.next_direction == 'right':
                temp_x += self.speed
            
            # Create a temporary rect to check collision
            temp_rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
            temp_rect.center = (temp_x, temp_y)
            
            if not self.maze.check_collision(temp_rect):
                self.direction = self.next_direction
                self.next_direction = None
        
        # Move in current direction if possible
        temp_x, temp_y = self.x, self.y
        
        if self.direction == 'up':
            temp_y -= self.speed
        elif self.direction == 'down':
            temp_y += self.speed
        elif self.direction == 'left':
            temp_x -= self.speed
        elif self.direction == 'right':
            temp_x += self.speed
        
        # Create a temporary rect to check collision
        temp_rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        temp_rect.center = (temp_x, temp_y)
        
        if not self.maze.check_collision(temp_rect):
            self.x, self.y = temp_x, temp_y
            self.rect.center = (self.x, self.y)
        
        # Update animation
        self.animation_count += 1
        if self.animation_count >= 5:
            self.animation_count = 0
            self.open_close = (self.open_close + 1) % 3
            
        # Update the sprite image
        self._draw_pacman_image()
    
    def _draw_pacman_image(self):
        """Draw Pacman as a simple rectangle"""
        # Clear the surface with transparent background
        self.image.fill((0, 0, 0, 0))
        
        # Draw the rectangle body
        rect_width = self.radius * 2
        rect_height = self.radius * 2
        rect = pygame.Rect(0, 0, rect_width, rect_height)
        pygame.draw.rect(self.image, (255, 255, 0), rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # press any key to unfreeze Pacman
            if self.frozen and event.key:
                self.frozen = False
                self._draw_pacman_image()  # Redraw when unfreezing

            if not self.frozen:
                if event.key == pygame.K_UP:
                    self.change_direction('up')
                elif event.key == pygame.K_DOWN:
                    self.change_direction('down')
                elif event.key == pygame.K_LEFT:
                    self.change_direction('left')
                elif event.key == pygame.K_RIGHT:
                    self.change_direction('right')