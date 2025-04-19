import pygame
import config
from pacman import Pacman
from maze import Maze
from ghost import Ghost
from datetime import datetime

def handle_game_end(screen, score, is_win=False):
    # Load appropriate image based on game outcome
    if is_win:
        end_image = pygame.image.load(config.ASSETS['YOU_WIN']).convert_alpha()
    else:
        end_image = pygame.image.load(config.ASSETS['GAME_OVER']).convert_alpha()
    
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
    # Initialize maze
    maze = Maze(cell_size, maze_layout)

    # Get initial entity positions
    initial_positions = maze.get_initial_entity_positions()

    # Initialize Pacman
    pacman_pos = initial_positions.get('M', (width // 2, (height - 50) // 2))
    pacman = Pacman(pacman_pos, cell_size, maze)

    # Initialize Sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(pacman)

    # Initialize Ghosts using initial positions and configuration
    ghost_types = ['P', 'R', 'O', 'B']
    for ghost_type in ghost_types:
        if ghost_type in initial_positions:
            ghost_class = config.GHOST_TYPES.get(ghost_type.lower().replace('p', 'pink').replace('r', 'red').replace('o', 'orange').replace('b', 'blue'))
            
            if ghost_class:
                ghost = ghost_class(initial_positions[ghost_type], cell_size, maze, pacman)
                ghost.debug_mode = config.GHOST_CONFIG['DEBUG']
                all_sprites.add(ghost)

    return maze, pacman, all_sprites

def main():
    pygame.init()

    # Define screen dimensions and maze layout using config
    WIDTH, HEIGHT = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
    MAZE = config.load_maze_layout()

    # Define maze dimensions and cell size
    CELL_SIZE = config.calculate_cell_size(WIDTH, HEIGHT, MAZE)

    # Use colors from config
    BLACK = config.COLORS['BLACK']

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
                # print("Congratulations! You ate all the dots!")
                game_active = handle_game_end(screen, score, is_win=True)
                break

            # Check for collisions with ghosts
            for ghost in Ghost.all_ghosts:
                if ghost.check_collision_with_pacman():
                    # Game over if any ghost catches Pacman
                    # print(f"Game Over! {ghost.__class__.__name__} caught you!")
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
            font = pygame.font.SysFont(None, config.SCORE_FONT['SIZE'])
            score_text = font.render(f"Score: {score}", True, config.SCORE_FONT['COLOR'])
            screen.blit(score_text, (10, 610))

            # Update the screen display
            pygame.display.flip()

            # Control the frame rate
            clock.tick(config.FRAME_RATE)

    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main()