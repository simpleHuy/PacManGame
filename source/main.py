import pygame
import os
from pacman import Pacman
from maze import Maze
from ghost import Ghost
from ghostImpl.organgeGhost import OrangeGhost
from ghostImpl.blueGhost import BlueGhost
from ghostImpl.redGhost import RedGhost

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


# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
maze = Maze(CELL_SIZE, MAZE)

# Initialize sprites and sprite group
all_sprites = pygame.sprite.Group()

pacman = Pacman((48, 36), CELL_SIZE, maze)
all_sprites.add(pacman)

ucs_ghost = OrangeGhost((48, 576 - 24), CELL_SIZE, maze, pacman)
bfs_ghost = BlueGhost((WIDTH // 2 - 48, 576 - 24), CELL_SIZE, maze, pacman)
astar_ghost = RedGhost((720 - 24, 576 - 24), CELL_SIZE, maze, pacman)

# Add all ghosts to the all_sprites group
all_sprites.add(Ghost.all_ghosts)

# Set debug mode for ghosts if needed
# ucs_ghost.toggle_debug()
# bfs_ghost.toggle_debug()
# astar_ghost.toggle_debug()

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
    pacman.update()
    Ghost.update_all()
        
    score += maze.check_dot_collision(pacman.rect)

    # Check for collisions with ghosts
    game_over = False
    for ghost in Ghost.all_ghosts:
        if ghost.check_collision_with_pacman():
            # Game over if any ghost catches Pacman
            print(f"Game Over! {ghost.__class__.__name__} caught you!")
            game_over = True
            break

    if game_over:
        running = False

    # Draw
    maze.draw(screen)
    
    all_sprites.draw(screen)
    
    # Draw debug info for ghosts if enabled
    for ghost in Ghost.all_ghosts:
        if hasattr(ghost, 'debug_mode') and ghost.debug_mode:
            ghost.draw_debug(screen)

    # Score display
    font = pygame.font.SysFont(None, 40)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 610))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()