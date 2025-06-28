import time
import json
from config import *

class MazeUtils:
    @staticmethod
    def validate_maze_format(maze_data):
        """Validate that maze data is in correct format"""
        if not isinstance(maze_data, list):
            return False, "Maze must be a list"
        
        if not isinstance(maze_data, list):
            return False, "Maze must be a list"
        if not maze_data:
            return False, "Maze cannot be empty"
        
        rows= len(maze_data)
        cols= len(maze_data[0]) if rows > 0 else 0

        for i, row in enumerate(maze_data):
            if len(row) != cols:
                return False, f"Row{i} has a different length than row 0 "
            
            start_count=0
            goal_count=0

            for row in maze_data:
                for cell in row:
                    if cell == START:
                        start_count += 1
                    elif cell == GOAL:
                        goal_count += 1
                    elif cell not in [WALL, FREE]:
                        return False, f"Invalid cell value {cell} "
                    
                    if start_count != 1:
                        return False, "Maze must have exactly one start position (S)"
                    if goal_count != 1:
                        return False, "Maze must have exactly one goal position (G)"