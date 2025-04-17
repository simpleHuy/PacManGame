import pygame
import math

class Pacman:
    def __init__(self, position, CELL_SIZE):
        self.x, self.y = position
        self.radius = int(CELL_SIZE * 0.5)
        # Scale speed relative to cell size too
        self.speed = max(1, int(CELL_SIZE / 8))
        self.direction = 'right'  # Initial direction
        self.next_direction = None
        self.animation_count = 0
        self.open_close = 0  # Animation state (0: closed, 1: half open, 2: fully open)
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                              self.radius * 2, self.radius * 2)
        self.frozen = True  # Pacman starts frozen
    
    def change_direction(self, new_direction):
        # Store next direction, will change when possible
        self.next_direction = new_direction
    
    def update(self, maze):
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
            
            temp_rect = pygame.Rect(temp_x - self.radius, temp_y - self.radius, 
                                   self.radius * 2, self.radius * 2)
            
            if not maze.check_collision(temp_rect):
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
        
        temp_rect = pygame.Rect(temp_x - self.radius, temp_y - self.radius, 
                              self.radius * 2, self.radius * 2)
        
        if not maze.check_collision(temp_rect):
            self.x, self.y = temp_x, temp_y
            self.rect = temp_rect
        
        # Update animation
        self.animation_count += 1
        if self.animation_count >= 5:
            self.animation_count = 0
            self.open_close = (self.open_close + 1) % 3
    
    def draw(self, screen):
        # Draw Pac-Man with animation
        if self.open_close == 0:  # Fully open (circle)
            pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)
        else:
            # Calculate angle based on direction
            start_angle = 0
            if self.direction == 'right':
                start_angle = 0
            elif self.direction == 'down':
                start_angle = 90
            elif self.direction == 'left':
                start_angle = 180
            elif self.direction == 'up':
                start_angle = 270
                
            # Animation angles
            mouth_size = 45 if self.open_close == 1 else 90  # Degrees
            
            pygame.draw.arc(screen, (255, 255, 0), 
                         (self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2),
                         math.radians(start_angle + mouth_size/2), 
                         math.radians(start_angle + 360 - mouth_size/2), 
                         self.radius)
            
            # Draw eye
            eye_x = self.x + self.radius * 0.4 * math.cos(math.radians(start_angle - 90))
            eye_y = self.y + self.radius * 0.4 * math.sin(math.radians(start_angle - 90))
            pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 3)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # press any key to unfreeze Pacman
            if self.frozen and event.key:
                self.frozen = False

            if not self.frozen:
                if event.key == pygame.K_UP:
                    self.change_direction('up')
                elif event.key == pygame.K_DOWN:
                    self.change_direction('down')
                elif event.key == pygame.K_LEFT:
                    self.change_direction('left')
                elif event.key == pygame.K_RIGHT:
                    self.change_direction('right')
