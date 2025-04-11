import pygame

class PacMan:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed  # Small movement speed (0.5)
        self.direction = pygame.Vector2(0, 0)  # Initial direction is stationary
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self, walls, pellets):
        # Calculate Pac-Man's future position based on the direction and speed
        future_position = self.rect.move(self.direction.x * self.speed, self.direction.y * self.speed)
        
        # Check if Pac-Man will collide with any walls
        for wall in walls:
            if future_position.colliderect(wall):  # Check for collision with walls
                # If there is a collision, stop Pac-Man from moving in that direction
                if self.direction.x != 0:
                    self.direction.x = 0  # Stop horizontal movement if there's a horizontal collision
                if self.direction.y != 0:
                    self.direction.y = 0  # Stop vertical movement if there's a vertical collision
                return
        # Check if Pac-Man will collide with any pellets and remove the pellet if there's a collision
        for pellet in pellets[:]:
            pellet_rect = pygame.Rect(pellet[0] - self.radius, pellet[1] - self.radius, self.radius * 2, self.radius * 2)
            if future_position.colliderect(pellet_rect):
                pellets.remove(pellet)  # Remove the pellet from the list if Pac-Man eats it
                return True

        # If no collision, update the position
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))  # Update the rect

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

    def update_direction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction = pygame.Vector2(-1, 0)  # Move left
            elif event.key == pygame.K_RIGHT:
                self.direction = pygame.Vector2(1, 0)  # Move right
            elif event.key == pygame.K_UP:
                self.direction = pygame.Vector2(0, -1)  # Move up
            elif event.key == pygame.K_DOWN:
                self.direction = pygame.Vector2(0, 1)  # Move down
