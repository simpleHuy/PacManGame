import pygame
import os

pygame.init()

# Define screen dimensions
WIDTH, HEIGHT = 600, 744

maze_path = os.path.join(os.path.dirname(__file__), "..", "input", "maze.txt")
with open(maze_path) as file:
    MAZE = [line.strip() for line in file.readlines()]

# Define maze dimensions and cell size
ROWS, COLS = len(MAZE), len(MAZE[0])
CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)
WALL_THICKNESS = CELL_SIZE // 6

# Define colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Transform maze into walls and pellets
walls = []
pellets = []
for row_idx, row in enumerate(MAZE):
    for col_idx, cell in enumerate(row):
        x, y = col_idx * CELL_SIZE, row_idx * CELL_SIZE
        if cell == "#":
            walls.append((x + WALL_THICKNESS, y + WALL_THICKNESS, CELL_SIZE - 0.5 * WALL_THICKNESS, CELL_SIZE - 0.5 * WALL_THICKNESS))  # Create a rectangle for the wall
        elif cell == ".":
            pellets.append((x + CELL_SIZE // 2, y + CELL_SIZE // 2)) # Create a circle for the pellet

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Maze")

running = True
while running:
    screen.fill(BLACK)
    
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)
    
    for pellet in pellets:
        pygame.draw.circle(screen, YELLOW, pellet, CELL_SIZE // 6)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()

pygame.quit()
