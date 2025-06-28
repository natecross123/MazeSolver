# maze.py
# Maze representation and data structure handling

from config import *
import random

class Maze:
    def __init__(self, rows=MAZE_ROWS, cols=MAZE_COLS):
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.start = None
        self.goal = None
        self.generate_maze()
    
    def generate_maze(self):
        """Generate a sample maze with walls, free spaces, start, and goal"""
        # Initialize with all free spaces
        self.grid = [[FREE for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Add border walls
        for i in range(self.rows):
            self.grid[i][0] = WALL  # Left border
            self.grid[i][self.cols-1] = WALL  # Right border
        
        for j in range(self.cols):
            self.grid[0][j] = WALL  # Top border
            self.grid[self.rows-1][j] = WALL  # Bottom border
        
        # Add some random internal walls
        for i in range(2, self.rows-2):
            for j in range(2, self.cols-2):
                if random.random() < 0.3:  # 30% chance of wall
                    self.grid[i][j] = WALL
        
        # Set start and goal positions
        self.start = (1, 1)
        self.goal = (self.rows-2, self.cols-2)
        self.grid[self.start[0]][self.start[1]] = START
        self.grid[self.goal[0]][self.goal[1]] = GOAL
        
        # Ensure path exists by clearing a simple path
        self._ensure_path_exists()
    
    def _ensure_path_exists(self):
        """Ensure there's at least one path from start to goal"""
        # Clear a simple L-shaped path
        row, col = self.start
        goal_row, goal_col = self.goal
        
        # Horizontal path
        while col != goal_col:
            if col < goal_col:
                col += 1
            else:
                col -= 1
            if self.grid[row][col] == WALL:
                self.grid[row][col] = FREE
        
        # Vertical path
        while row != goal_row:
            if row < goal_row:
                row += 1
            else:
                row -= 1
            if self.grid[row][col] == WALL:
                self.grid[row][col] = FREE
    
    def load_from_list(self, maze_list):
        """Load maze from a 2D list"""
        self.rows = len(maze_list)
        self.cols = len(maze_list[0]) if maze_list else 0
        self.grid = [row[:] for row in maze_list]  # Deep copy
        
        # Find start and goal positions
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == START:
                    self.start = (i, j)
                elif self.grid[i][j] == GOAL:
                    self.goal = (i, j)
    
    def is_valid_position(self, row, col):
        """Check if position is within maze bounds"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def is_free_space(self, row, col):
        """Check if position is a free space (not a wall)"""
        if not self.is_valid_position(row, col):
            return False
        return self.grid[row][col] != WALL
    
    def get_neighbors(self, row, col):
        """Get valid neighboring positions"""
        neighbors = []
        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            if self.is_free_space(new_row, new_col):
                neighbors.append((new_row, new_col))
        return neighbors
    
    def get_cell_value(self, row, col):
        """Get the value at a specific cell"""
        if self.is_valid_position(row, col):
            return self.grid[row][col]
        return None
    
    def validate_maze(self):
        """Validate that maze has start and goal positions"""
        if self.start is None:
            raise ValueError("Maze must have a start position (S)")
        if self.goal is None:
            raise ValueError("Maze must have a goal position (G)")
        return True
    
    def reset_maze(self):
        """Reset maze to initial state (remove visited markers)"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] not in [WALL, START, GOAL]:
                    self.grid[i][j] = FREE
    
    def print_maze(self):
        """Print maze to console for debugging"""
        for row in self.grid:
            print(''.join(str(cell) if cell != FREE else '.' for cell in row))
    
    def get_sample_maze(self):
        """Return a predefined sample maze for testing"""
        sample = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 'S', 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 'G', 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        return sample