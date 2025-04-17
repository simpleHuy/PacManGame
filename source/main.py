import pygame
import os
from pacman import PacMan
from blueGhost import BlueGhost
from A_star import RedGhost


pygame.init()

# Define screen dimensions
WIDTH, HEIGHT = 744, 650
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

# Font for displaying score
font = pygame.font.Font(None, 36)

# Transform maze into walls and pellets
walls = []
pellets = []
for row_idx, row in enumerate(MAZE):
    for col_idx, cell in enumerate(row):
        x, y = col_idx * CELL_SIZE, row_idx * CELL_SIZE
        if cell == "#":
            walls.append((x, y, CELL_SIZE, CELL_SIZE))  # Create a rectangle for the wall
        elif cell == ".":
            pellets.append((x + CELL_SIZE // 2, y + CELL_SIZE // 2)) # Create a circle for the pellet

# Initialize
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Maze")
pacman = PacMan(WIDTH // 2, (HEIGHT -  50) // 2, CELL_SIZE // 3.3, 3)
blue_ghost = BlueGhost(
    x=1 * CELL_SIZE + CELL_SIZE // 2,
    y=1 * CELL_SIZE + CELL_SIZE // 2,
    radius=CELL_SIZE // 3,
    speed=1.5,
    maze=MAZE,
    cell_size=CELL_SIZE
)


# Khởi tạo con redghost có trúc trúc như bên dưới-----
redghost = RedGhost(color=(255, 0, 0), start_position=(33, 33), maze=MAZE,size=(CELL_SIZE // 3.3,CELL_SIZE // 3.3),speed = 0,cell_size= CELL_SIZE)

clock = pygame.time.Clock()

#Innitialize RedGhost



# Running game loop
running = True
score = 0 

#flag = 0
while running:
    screen.fill(BLACK)
    
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)
    
    for pellet in pellets:
        pygame.draw.circle(screen, YELLOW, pellet, CELL_SIZE // 8)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pacman.update_direction(event)
    
    # Move Pac-Man and draw it on the screen
    if pacman.move(walls, pellets):
        score += 10  # Increase score when a pellet is eaten
    pacman.draw(screen)
    '''
    Đoạn này để phòng hờ
    flag += 1
    if flag == CELL_SIZE:
      redghost.update((pacman.x,pacman.y))
      redghost.move()
      flag =0
    '''
  
   # Cập nhật cách chạy cho redghost theo vị trí của pacman và cho nó di chuyển 1 bước, vẽ redghost
    redghost.update((pacman.x,pacman.y))
    redghost.move()
    redghost.draw(screen)
  
    # Display the score at the bottom-left corner of the screen
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))  # Place score at the bottom-left corner

    blue_ghost.update((pacman.x, pacman.y))
    blue_ghost.move()
    blue_ghost.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()