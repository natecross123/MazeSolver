# config.py
# Constants and configuration settings for the maze solver

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Maze Solver - BFS, DFS, A*"

# Cell size and maze dimensions
CELL_SIZE = 20
MAZE_ROWS = 25
MAZE_COLS = 35

# Colors
COLORS = {
    'WALL': 'black',
    'FREE': 'white',
    'START': 'green',
    'GOAL': 'red',
    'VISITED_BFS': 'lightblue',
    'VISITED_DFS': 'lightyellow',
    'VISITED_ASTAR': 'lightcoral',
    'PATH': 'orange',
    'GRID_LINE': 'gray'
}

# Animation settings
ANIMATION_SPEED = 0.1  # seconds between steps
FAST_SPEED = 0.01
SLOW_SPEED = 0.3

# Maze symbols
WALL = 1
FREE = 0
START = 'S'
GOAL = 'G'

# Algorithm types
ALGORITHMS = {
    'BFS': 1,
    'DFS': 2,
    'ASTAR': 3
}

# Directions for movement (right, down, left, up)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Key bindings
KEY_BINDINGS = {
    '1': 'BFS',
    '2': 'DFS',
    '3': 'A*',
    'r': 'RESET',
    'q': 'QUIT',
    'plus': 'SPEED_UP',
    'minus': 'SLOW_DOWN'
}