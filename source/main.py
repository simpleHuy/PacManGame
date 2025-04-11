import pygame
import os
from pacman import Pacman
from maze import Maze
from ucs_ghost import UCSGhost

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


# Initialize
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Maze")
pacman = Pacman((WIDTH // 2, (HEIGHT -  50) // 2), CELL_SIZE)
maze = Maze(CELL_SIZE, MAZE)
ucs_ghost = UCSGhost((WIDTH // 4, HEIGHT // 4), CELL_SIZE, maze)
ucs_ghost.set_target(pacman)
clock = pygame.time.Clock()

# Running game loop
running = True
score = 0 
while running:
    screen.fill(BLACK)

    # Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pacman.handle_event(event)

    # Update
    pacman.update(maze)
    ucs_ghost.update()
    score += maze.check_dot_collision(pacman.rect)

    if ucs_ghost.check_collision_with_pacman():
        # Game over if ghost catches Pacman
        # You can implement a proper game over screen here
        print("Game Over! Ghost caught you!")
        running = False

    # Draw
    maze.draw(screen)
    pacman.draw(screen)
    ucs_ghost.draw(screen)
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()