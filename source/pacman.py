import pygame
import math
import os

class Pacman(pygame.sprite.Sprite):
    def __init__(self, position, cell_size, maze):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.radius = int(cell_size * 0.5)
        self.cell_size = cell_size
        
        # Load base Pacman images
        self.base_images = self.load_pacman_images(cell_size)
        
        # Scale speed relative to cell size
        self.speed = max(1, int(cell_size / 8))
        self.direction = 'right'  # Initial direction
        self.next_direction = None
        self.animation_count = 0
        self.mouth_state = 0  # 0: 1.png, 1: 2.png, 2: 3.png
        
        # Rotation angles for different directions
        self.rotation_angles = {
            'right': 0,
            'up': 90,
            'left': 180,
            'down': 270
        }
        
        # Create rotated images for each direction and mouth state
        self.directional_images = self.create_rotated_images()
        
        # Initial image
        self.image = self.directional_images['right'][self.mouth_state]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.frozen = True  # Pacman starts frozen
        self.maze = maze  # Store maze reference for collision detection

    def create_rotated_images(self):
        """
        Create rotated images for each direction based on base images
        """
        rotated_images = {}
        for direction, angle in self.rotation_angles.items():
            direction_images = []
            for base_image in self.base_images:
                # Rotate the base image
                rotated_image = pygame.transform.rotate(base_image, angle)
                direction_images.append(rotated_image)
            rotated_images[direction] = direction_images
        return rotated_images

    @classmethod
    def load_pacman_images(cls, cell_size):
        """
        Load base Pacman images for mouth animation
        
        Args:
            cell_size (int): Size to scale the images to
        
        Returns:
            list: List of mouth state images
        """
        try:
            # Try multiple possible base paths
            base_paths = [
                os.path.join('assets', 'pacman'),
                'assets/pacman'
            ]
            
            for base_path in base_paths:
                mouth_states = ['1.png', '2.png', '3.png']
                images = []
                
                for mouth_image in mouth_states:
                    file_path = os.path.join(base_path, mouth_image)
                    
                    if os.path.exists(file_path):
                        # Load image
                        original_image = pygame.image.load(file_path).convert_alpha()
                        
                        # Scale image to cell size
                        scaled_image = pygame.transform.scale(original_image, (cell_size, cell_size))
                        
                        images.append(scaled_image)
                
                # If we found all 3 images, return them
                if len(images) == 3:
                    return images
            
            # If no images found, create fallback images
            print("Creating fallback Pacman images")
            fallback_images = []
            for i in range(3):
                fallback_image = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                fallback_image.fill((0, 0, 0, 0))  # Transparent background
                
                # Draw Pacman with different mouth openings
                center = (cell_size // 2, cell_size // 2)
                radius = cell_size // 2
                
                # Base yellow color
                color = (255, 255, 0)
                
                # Draw full circle
                pygame.draw.circle(fallback_image, color, center, radius)
                
                # Create mouth effect based on state
                if i > 0:
                    # Create mouth opening
                    mouth_points = [
                        center,
                        (center[0] + radius * math.cos(math.pi / 4), 
                         center[1] + radius * math.sin(math.pi / 4)),
                        (center[0] + radius * math.cos(-math.pi / 4), 
                         center[1] + radius * math.sin(-math.pi / 4))
                    ]
                    pygame.draw.polygon(fallback_image, (0, 0, 0), mouth_points)
                
                fallback_images.append(fallback_image)
            
            return fallback_images
        
        except Exception as e:
            print(f"Error loading Pacman images: {e}")
            return None

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
            self.mouth_state = (self.mouth_state + 1) % 3
            
        # Update the sprite image with current direction and mouth state
        self.image = self.directional_images[self.direction][self.mouth_state]

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