# maze.py
# Simple, clean maze generator - creates readable mazes like in the image

from config import *
import random

class Maze:
    def __init__(self, rows=15, cols=20):  # Smaller, cleaner size
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.start = None
        self.goal = None
        self.generate_simple_maze()
    
    def generate_simple_maze(self):
        """Generate a simple, clean maze like in the image"""
        # Choose random maze style
        maze_type = random.choice(['pattern', 'classroom', 'random'])
        
        if maze_type == 'pattern':
            self._generate_pattern_maze()
        elif maze_type == 'classroom':
            self._generate_classroom_maze()
        else:
            self._generate_random_maze()
    
    def _generate_pattern_maze(self):
        """Generate maze with regular patterns"""
        # Initialize with all free spaces
        self.grid = [[FREE for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Add border walls
        self._add_borders()
        
        # Add pattern-based walls
        for col in range(3, self.cols-3, 4):  # Every 4th column
            for row in range(2, self.rows-2):
                if random.random() < 0.6:
                    self.grid[row][col] = WALL
        
        for row in range(3, self.rows-3, 4):  # Every 4th row
            for col in range(2, self.cols-2):
                if random.random() < 0.4:
                    self.grid[row][col] = WALL
        
        self._set_start_goal()
        self._create_guaranteed_path()
    
    def _generate_classroom_maze(self):
        """Generate classroom-style maze"""
        self.grid = [[FREE for _ in range(self.cols)] for _ in range(self.rows)]
        self._add_borders()
        
        # Create specific patterns like classroom examples
        patterns = [
            # L-shaped barriers
            [(3, 5), (4, 5), (5, 5), (5, 6), (5, 7)],
            [(7, 8), (8, 8), (9, 8), (10, 8)],
            [(3, 12), (4, 12), (5, 12), (6, 12)],
            
            # T-shaped barriers
            [(8, 3), (8, 4), (8, 5), (7, 4), (9, 4)],
            [(5, 15), (6, 15), (7, 15), (6, 14), (6, 16)]
        ]
        
        # Randomly select and apply some patterns
        selected_patterns = random.sample(patterns, random.randint(2, 4))
        for pattern in selected_patterns:
            for row, col in pattern:
                if self._is_valid_wall_position(row, col):
                    self.grid[row][col] = WALL
        
        self._set_start_goal()
        self._create_guaranteed_path()
    
    def _generate_random_maze(self):
        """Generate more random maze"""
        self.grid = [[FREE for _ in range(self.cols)] for _ in range(self.rows)]
        self._add_borders()
        
        # Add random walls with some structure
        for row in range(2, self.rows-2):
            for col in range(2, self.cols-2):
                if random.random() < 0.25:  # 25% chance of wall
                    self.grid[row][col] = WALL
        
        self._set_start_goal()
        self._create_guaranteed_path()
    
    def _add_borders(self):
        """Add border walls"""
        for i in range(self.rows):
            self.grid[i][0] = WALL
            self.grid[i][self.cols-1] = WALL
        for j in range(self.cols):
            self.grid[0][j] = WALL
            self.grid[self.rows-1][j] = WALL
    
    def _set_start_goal(self):
        """Set start and goal positions"""
        self.start = (1, 1)
        self.goal = (self.rows-2, self.cols-2)
        self.grid[self.start[0]][self.start[1]] = START
        self.grid[self.goal[0]][self.goal[1]] = GOAL
    
    def _is_valid_wall_position(self, row, col):
        """Check if it's valid to place a wall here"""
        return (0 < row < self.rows-1) and (0 < col < self.cols-1)
    
    def generate_maze_by_difficulty(self, difficulty='medium'):
        """Generate maze based on difficulty level"""
        if difficulty == 'easy':
            self._generate_easy_maze()
        elif difficulty == 'hard':
            self._generate_hard_maze()
        else:  # medium
            self.generate_simple_maze()
    
    def _generate_easy_maze(self):
        """Generate an easy maze with fewer walls"""
        self.grid = [[FREE for _ in range(self.cols)] for _ in range(self.rows)]
        self._add_borders()
        
        # Add minimal walls - mostly straight paths
        for row in range(3, self.rows-3, 6):
            for col in range(3, self.cols-3):
                if random.random() < 0.3:
                    self.grid[row][col] = WALL
        
        self._set_start_goal()
        self._create_guaranteed_path()
    
    def _generate_hard_maze(self):
        """Generate a harder maze with more walls and complexity"""
        self.grid = [[FREE for _ in range(self.cols)] for _ in range(self.rows)]
        self._add_borders()
        
        # Add more walls and complex patterns
        for row in range(2, self.rows-2):
            for col in range(2, self.cols-2):
                if random.random() < 0.35:  # More walls
                    self.grid[row][col] = WALL
        
        # Add some corridor patterns
        for i in range(3):
            start_row = random.randint(2, self.rows-3)
            start_col = random.randint(2, self.cols-3)
            length = random.randint(3, 6)
            
            if random.choice([True, False]):  # Horizontal corridor
                for c in range(start_col, min(start_col + length, self.cols-2)):
                    if self._is_valid_wall_position(start_row, c):
                        self.grid[start_row][c] = WALL
            else:  # Vertical corridor
                for r in range(start_row, min(start_row + length, self.rows-2)):
                    if self._is_valid_wall_position(r, start_col):
                        self.grid[r][start_col] = WALL
        
        self._set_start_goal()
        self._create_guaranteed_path()
    
    def generate_maze_with_size(self, new_rows, new_cols):
        """Generate a maze with custom size"""
        self.rows = max(10, min(30, new_rows))  # Limit size for display
        self.cols = max(15, min(40, new_cols))
        self.generate_simple_maze()
    
    def get_predefined_mazes(self):
        """Get a collection of predefined interesting mazes"""
        mazes = {
            'simple': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 'S', 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 'G', 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ],
            
            'spiral': [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 'S', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 'G', 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        }
        return mazes
    
    def _create_guaranteed_path(self):
        """Create a guaranteed path from start to goal"""
        # Simple L-shaped path to ensure solvability
        row, col = self.start
        goal_row, goal_col = self.goal
        
        # Clear horizontal path first
        current_col = col
        while current_col != goal_col:
            if current_col < goal_col:
                current_col += 1
            else:
                current_col -= 1
            
            # Don't overwrite start/goal
            if (row, current_col) not in [self.start, self.goal]:
                self.grid[row][current_col] = FREE
        
        # Clear vertical path
        current_row = row
        while current_row != goal_row:
            if current_row < goal_row:
                current_row += 1
            else:
                current_row -= 1
            
            # Don't overwrite start/goal
            if (current_row, goal_col) not in [self.start, self.goal]:
                self.grid[current_row][goal_col] = FREE
    
    def create_classroom_style_maze(self):
        """Create a maze similar to the classroom examples"""
        # Start with all free spaces
        self.grid = [[FREE for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Add outer walls
        for i in range(self.rows):
            self.grid[i][0] = WALL
            self.grid[i][self.cols-1] = WALL
        for j in range(self.cols):
            self.grid[0][j] = WALL
            self.grid[self.rows-1][j] = WALL
        
        # Create a simple pattern like in classroom examples
        # Add some strategic walls to create interesting paths
        wall_patterns = [
            # Some vertical barriers
            [(3, 5), (4, 5), (5, 5)],
            [(7, 8), (8, 8), (9, 8)],
            [(3, 12), (4, 12), (5, 12), (6, 12)],
            
            # Some horizontal barriers
            [(6, 3), (6, 4), (6, 5)],
            [(10, 8), (10, 9), (10, 10), (10, 11)],
            [(4, 15), (4, 16), (4, 17)]
        ]
        
        # Apply wall patterns if they fit in the maze
        for pattern in wall_patterns:
            for row, col in pattern:
                if (0 < row < self.rows-1) and (0 < col < self.cols-1):
                    self.grid[row][col] = WALL
        
        # Set start and goal
        self.start = (1, 1)
        self.goal = (self.rows-2, self.cols-2)
        self.grid[self.start[0]][self.start[1]] = START
        self.grid[self.goal[0]][self.goal[1]] = GOAL
        
        # Ensure path exists
        self._create_guaranteed_path()
    
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
        print("\nMaze Layout:")
        for row in self.grid:
            line = ""
            for cell in row:
                if cell == WALL:
                    line += "█"
                elif cell == START:
                    line += "S"
                elif cell == GOAL:
                    line += "G"
                else:
                    line += " "
            print(line)
        print()
    
    def get_simple_test_maze(self):
        """Return a very simple test maze"""
        simple = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 'S', 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 'G', 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        return simple