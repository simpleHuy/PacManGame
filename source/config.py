import os
from typing import Dict, Type, Optional, Tuple
from ghostImpl.organgeGhost import OrangeGhost
from ghostImpl.blueGhost import BlueGhost
from ghostImpl.redGhost import RedGhost
from ghostImpl.pinkGhost import PinkGhost
from ghost import Ghost

# Screen Configuration
SCREEN_WIDTH = 744
SCREEN_HEIGHT = 650

# Maze Configuration
MAZE_PATH = os.path.join(os.path.dirname(__file__), "..", "input", "maze.txt")

# Colors
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'ORANGE': (255, 165, 0),
    'PINK': (255, 192, 203),

    'WALL': (0, 40, 255),
    'DOT': (255, 255, 255)
}

# Game Settings
FRAME_RATE = 60
CELL_SIZE = None  # Will be calculated dynamically based on screen and maze dimensions

# Asset Paths
ASSETS = {
    'GAME_OVER': 'assets/game-over.png',
    'YOU_WIN': 'assets/you-win.jpg'
}

# Text Configuration
SCORE_FONT = {
    'SIZE': 40,
    'COLOR': COLORS['WHITE']
}
# Pacman Configuration
PACMAN_CONFIG = {
    'SPEED': 3,
}

# Ghost Configuration
GHOST_CONFIG = {
    # Global debug mode setting
    'DEBUG': True,
    'SPEED': 1  # Speed of the ghosts
}

# Predefined Ghost Types
GHOST_TYPES = {
    'orange': OrangeGhost,
    'blue': BlueGhost,
    'pink': PinkGhost,
    'red': RedGhost
}

def calculate_cell_size(width, height, maze_layout):
    """
    Calculate the optimal cell size based on screen dimensions and maze layout
    
    Args:
        width (int): Screen width
        height (int): Screen height
        maze_layout (list): Maze layout
    
    Returns:
        int: Optimal cell size
    """
    rows = len(maze_layout)
    cols = len(maze_layout[0])
    return min(width // cols, height // rows)

def load_maze_layout():
    """
    Load maze layout from file
    
    Returns:
        list: Maze layout as a list of strings
    """
    with open(MAZE_PATH) as file:
        return [line.strip() for line in file.readlines()]