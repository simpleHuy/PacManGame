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
    # Enable/Disable specific ghosts
    'GHOSTS': {
        'orange': False,
        'blue': False,
        'pink': True,
        'red': False
    },
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

# Ghost Configuration
class GhostManager:
    """
    Manages ghost initialization and tracking with flexible configuration
    """
    def __init__(self, config: Dict):
        # Clear any existing ghosts
        Ghost.all_ghosts.empty()
        
        # Store configuration
        self.config = config
        
        # Dictionary to store ghost instances
        self.ghosts: Dict[str, Ghost] = {}
        
        # Predefined ghost positions
        self.default_positions = {
            'orange': (48, 576 - 24),
            'blue': lambda width: (width // 2 - 48, 576 - 24),
            'pink': (48, 36),
            'red': lambda width: (width - 24, 576 - 24)
        }

    def create_ghost(
        self, 
        ghost_type: str, 
        position: Optional[Tuple[int, int]] = None, 
        cell_size: Optional[int] = None, 
        maze = None, 
        pacman = None
    ):
        """
        Create a specific type of ghost based on configuration
        
        Args:
            ghost_type (str): Type of ghost to create (lowercase)
            position (tuple, optional): Custom position 
            cell_size (int, optional): Cell size
            maze (Maze, optional): Game maze
            pacman (Pacman, optional): Pacman instance
        
        Returns:
            Ghost or None: Created ghost instance or None if not enabled
        """
        # Validate ghost type
        if ghost_type.lower() not in GHOST_TYPES:
            raise ValueError(f"Invalid ghost type: {ghost_type}. Available types: {list(GHOST_TYPES.keys())}")
        
        # Check if ghost is enabled in configuration
        if not self.config['GHOSTS'].get(ghost_type.lower(), False):
            return None
        
        # Determine position
        if position is None:
            pos = self.default_positions[ghost_type.lower()]
            # If position is a lambda, call it with screen width
            position = pos(SCREEN_WIDTH) if callable(pos) else pos
        
        # Create ghost instance
        ghost_class = GHOST_TYPES[ghost_type.lower()]
        ghost = ghost_class(position, cell_size, maze, pacman)
        
        # Apply global debug setting if configured
        if self.config.get('DEBUG', False):
            ghost.toggle_debug()
        
        # Store ghost instance
        self.ghosts[ghost_type.lower()] = ghost
        
        return ghost

    def get_ghost(self, ghost_type: str) -> Optional[Ghost]:
        """
        Retrieve a specific ghost instance
        
        Args:
            ghost_type (str): Type of ghost to retrieve
        
        Returns:
            Ghost or None: Ghost instance if exists
        """
        return self.ghosts.get(ghost_type.lower())

    def toggle_debug(self, ghost_type: Optional[str] = None):
        """
        Toggle debug mode for a specific ghost or all ghosts
        
        Args:
            ghost_type (str, optional): Specific ghost type to toggle debug
        """
        if ghost_type:
            # Toggle debug for specific ghost
            ghost = self.get_ghost(ghost_type)
            if ghost:
                ghost.toggle_debug()
        else:
            # Toggle debug for all existing ghosts
            for ghost in self.ghosts.values():
                ghost.toggle_debug()

    def initialize(self, width, height, cell_size, maze, pacman):
        """
        Initialize all configured ghost types
        
        Args:
            width (int): Screen width
            height (int): Screen height
            cell_size (int): Size of each cell
            maze (Maze): Game maze object
            pacman (Pacman): Pacman instance
        
        Returns:
            pygame.sprite.Group: Group of all created ghosts
        """
        # Clear existing ghosts
        Ghost.all_ghosts.empty()
        self.ghosts.clear()

        # Create configured ghost types
        for ghost_type in GHOST_TYPES:
            self.create_ghost(
                ghost_type, 
                cell_size=cell_size, 
                maze=maze, 
                pacman=pacman
            )

        return Ghost.all_ghosts

# Create a global ghost manager
ghost_manager = GhostManager(GHOST_CONFIG)

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