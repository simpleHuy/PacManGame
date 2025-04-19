import pygame
import os
from pacman import Pacman
from maze import Maze
from ghost import Ghost
from ghostImpl.organgeGhost import OrangeGhost
from ghostImpl.blueGhost import BlueGhost
from ghostImpl.redGhost import RedGhost
from ghostImpl.pinkGhost import PinkGhost

def handle_game_end(screen, score, is_win=False):
    """
    Display game end screen (win or lose)
    
    Args:
        screen (pygame.Surface): The main game screen
        score (int): Final game score
        is_win (bool): Whether the player won the game
    
    Returns:
        bool: Whether to restart the game
    """
    # Load appropriate image based on game outcome
    if is_win:
        end_image = pygame.image.load('assets/you-win.jpg').convert_alpha()
    else:
        end_image = pygame.image.load('assets/game-over.png').convert_alpha()
    
    # Screen dimensions
    screen_width = screen.get_width()
    aspect_ratio = end_image.get_width() / end_image.get_height()
    scaled_height = int(screen_width / aspect_ratio)
    
    # Scale image
    end_image = pygame.transform.scale(end_image, (screen_width, scaled_height))
    
    # Display end image
    screen.blit(end_image, (0, (screen.get_height() - end_image.get_height()) // 2))
    pygame.display.flip()
    
    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                # ESC key to close game
                if event.key == pygame.K_ESCAPE:
                    return False
                # Any other key to restart
                return True
    
    return False

def initialize_game_objects(width, height, maze_layout, cell_size):
    """
    Initialize game objects
    
    Args:
        width (int): Screen width
        height (int): Screen height
        maze_layout (list): Maze layout
        cell_size (int): Size of each cell
    
    Returns:
        tuple: Initialized game objects
    """
    # Initialize maze
    maze = Maze(cell_size, maze_layout)

    # Initialize sprites and sprite group
    all_sprites = pygame.sprite.Group()

    # Initialize Pacman
    pacman = Pacman((width // 2, (height - 50) // 2), cell_size, maze)
    all_sprites.add(pacman)

    # Clear any existing ghosts
    Ghost.all_ghosts.empty()

    # Initialize Ghosts
    OrangeGhost((48, 576 - 24), cell_size, maze, pacman)
    BlueGhost((width // 2 - 48, 576 - 24), cell_size, maze, pacman)
    PinkGhost((48, 36), cell_size, maze, pacman)
    RedGhost((720 - 24, 576 - 24), cell_size, maze, pacman)

    # Add all ghosts to the all_sprites group
    all_sprites.add(Ghost.all_ghosts)

    return maze, pacman, all_sprites

def main():
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
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Initialize game
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")

    # Game loop
    running = True
    while running:
        # Initialize game objects
        maze, pacman, all_sprites = initialize_game_objects(WIDTH, HEIGHT, MAZE, CELL_SIZE)
        
        # Reset score
        score = 0
        clock = pygame.time.Clock()

        # Inner game loop
        game_active = True
        while game_active:
            screen.fill(BLACK)

            # Handle user input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False
                    running = False
                    break
                pacman.handle_event(event)

            # Update
            pacman.update()
            Ghost.update_all()
            
            # Check for dot collisions and update score
            score += maze.check_dot_collision(pacman.rect)

            # Check if all dots are eaten (win condition)
            if maze.are_all_dots_eaten():
                print("Congratulations! You ate all the dots!")
                game_active = handle_game_end(screen, score, is_win=True)
                break

            # Check for collisions with ghosts
            game_over = False
            for ghost in Ghost.all_ghosts:
                if ghost.check_collision_with_pacman():
                    # Game over if any ghost catches Pacman
                    print(f"Game Over! {ghost.__class__.__name__} caught you!")
                    game_active = handle_game_end(screen, score, is_win=False)
                    break

            if not game_active:
                running = False
                break

            # Draw the maze, Pacman, and Ghosts
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

            # Update the screen display
            pygame.display.flip()

            # Control the frame rate
            clock.tick(60)

    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main()