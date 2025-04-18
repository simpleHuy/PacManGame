import pygame
import os
from pacman import Pacman
from maze import Maze
from dfs_ghost import DFSGhost  # Import your DFSGhost class

pygame.init()

# Define screen dimensions
WIDTH, HEIGHT = 744, 650
maze_path = os.path.join(os.path.dirname(__file__), "..", "input", "maze.txt")
with open(maze_path) as file:
    MAZE = [line.strip() for line in file.readlines()]

# Define maze dimensions and cell size
ROWS, COLS = len(MAZE), len(MAZE[0])
CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)

# Define colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Maze with DFSGhost")

# Create Pacman object
pacman = Pacman((WIDTH // 2, (HEIGHT - 50) // 2), CELL_SIZE)

# Create maze object
maze = Maze(CELL_SIZE, MAZE)

# Create DFSGhost and set Pacman as the target
dfs_ghost = DFSGhost((WIDTH // 4, HEIGHT // 4), 10, 2, maze, CELL_SIZE, pacman)

# Initialize game clock
clock = pygame.time.Clock()

# Initialize game variables
running = True
score = 0

# Game loop
while running:
    screen.fill(BLACK)

    # Handle user input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pacman.handle_event(event)

    # Update game objects
    pacman.update(maze)
    dfs_ghost.update(pacman)  # Update DFSGhost based on Pacman

    # Check for dot collision in maze and update score
    score += maze.check_dot_collision(pacman.rect)

    # Check if the DFSGhost catches Pacman
    if dfs_ghost.check_collision_with_pacman():
        print("Game Over! DFSGhost caught you!")
        running = False

    # Draw the maze, Pacman, and DFSGhost
    maze.draw(screen)
    pacman.draw(screen)
    dfs_ghost.draw(screen)

    # Display the score
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the screen display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
