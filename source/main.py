import pygame
import os
from pacman import Pacman
from maze import Maze
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


# Initialize
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
pacman = Pacman((48, 36), CELL_SIZE)
maze = Maze(CELL_SIZE, MAZE)

# Initialize ghosts

ghosts = []
ucs_ghost = OrangeGhost((720 - 24, 576 - 24), CELL_SIZE, maze, pacman)
ghosts.append(ucs_ghost)
bfs_ghost = BlueGhost((720 - 24, 576 - 24), CELL_SIZE, maze, pacman)
ghosts.append(bfs_ghost)
astar_ghost = RedGhost((720 - 24, 576 - 24), CELL_SIZE, maze, pacman)
ghosts.append(astar_ghost)

# Set debug mode for ghosts
# for ghost in ghosts:
#     ghost.toggle_debug()


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
    for ghost in ghosts:
        ghost.update()
        
    score += maze.check_dot_collision(pacman.rect)

    game_over = False
    for ghost in ghosts:
        if ghost.check_collision_with_pacman():
            # Game over if any ghost catches Pacman
            print(f"Game Over! {ghost.__class__.__name__} caught you!")
            game_over = True
            break

    if game_over:
        running = False

    # Draw
    maze.draw(screen)
    pacman.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)

    font = pygame.font.SysFont(None, 40)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 610))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()