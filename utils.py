# utils.py
# Helper functions and utilities for the maze solver

import time
import json
from config import *

class MazeUtils:
    @staticmethod
    def validate_maze_format(maze_data):
        """Validate that maze data is in correct format"""
        if not isinstance(maze_data, list):
            return False, "Maze must be a list"
        
        if not maze_data:
            return False, "Maze cannot be empty"
        
        rows = len(maze_data)
        cols = len(maze_data[0]) if maze_data else 0
        
        # Check if all rows have same length
        for i, row in enumerate(maze_data):
            if len(row) != cols:
                return False, f"Row {i} has different length than row 0"
        
        # Check for start and goal
        start_count = 0
        goal_count = 0
        
        for row in maze_data:
            for cell in row:
                if cell == START:
                    start_count += 1
                elif cell == GOAL:
                    goal_count += 1
                elif cell not in [WALL, FREE]:
                    return False, f"Invalid cell value: {cell}"
        
        if start_count != 1:
            return False, f"Maze must have exactly one start position, found {start_count}"
        
        if goal_count != 1:
            return False, f"Maze must have exactly one goal position, found {goal_count}"
        
        return True, "Valid maze format"
    
    @staticmethod
    def load_maze_from_file(filename):
        """Load maze from a text file"""
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
            
            maze = []
            for line in lines:
                line = line.strip()
                if line:
                    row = []
                    for char in line:
                        if char == '#' or char == '1':
                            row.append(WALL)
                        elif char == '.' or char == '0':
                            row.append(FREE)
                        elif char.upper() == 'S':
                            row.append(START)
                        elif char.upper() == 'G':
                            row.append(GOAL)
                        else:
                            row.append(FREE)  # Default to free space
                    maze.append(row)
            
            return maze
        except FileNotFoundError:
            print(f"File {filename} not found")
            return None
        except Exception as e:
            print(f"Error loading maze from file: {e}")
            return None
    
    @staticmethod
    def save_maze_to_file(maze, filename):
        """Save maze to a text file"""
        try:
            with open(filename, 'w') as file:
                for row in maze.grid:
                    line = ""
                    for cell in row:
                        if cell == WALL:
                            line += "#"
                        elif cell == FREE:
                            line += "."
                        elif cell == START:
                            line += "S"
                        elif cell == GOAL:
                            line += "G"
                        else:
                            line += "."
                    file.write(line + "\n")
            print(f"Maze saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving maze to file: {e}")
            return False
    
    @staticmethod
    def save_statistics_to_file(stats_list, filename):
        """Save search statistics to JSON file"""
        try:
            with open(filename, 'w') as file:
                json.dump(stats_list, file, indent=2)
            print(f"Statistics saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving statistics: {e}")
            return False
    
    @staticmethod
    def create_sample_mazes():
        """Create various sample mazes for testing"""
        
        # Simple maze
        simple_maze = [
            [1, 1, 1, 1, 1],
            [1, 'S', 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 'G', 1],
            [1, 1, 1, 1, 1]
        ]
        
        # Complex maze
        complex_maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 'S', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'G', 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # No solution maze
        no_solution_maze = [
            [1, 1, 1, 1, 1],
            [1, 'S', 0, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 0, 'G', 1],
            [1, 1, 1, 1, 1]
        ]
        
        return {
            'simple': simple_maze,
            'complex': complex_maze,
            'no_solution': no_solution_maze
        }

class Timer:
    """Simple timer utility for measuring execution time"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer"""
        self.start_time = time.time()
    
    def stop(self):
        """Stop the timer"""
        self.end_time = time.time()
    
    def elapsed(self):
        """Get elapsed time in seconds"""
        if self.start_time is None:
            return 0
        
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def reset(self):
        """Reset the timer"""
        self.start_time = None
        self.end_time = None

class Logger:
    """Simple logging utility"""
    
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.enabled = True
    
    def log(self, message, level="INFO"):
        """Log a message"""
        if not self.enabled:
            return
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level}: {message}"
        
        print(log_message)
        
        if self.log_file:
            try:
                with open(self.log_file, 'a') as file:
                    file.write(log_message + "\n")
            except Exception as e:
                print(f"Error writing to log file: {e}")
    
    def info(self, message):
        """Log info message"""
        self.log(message, "INFO")
    
    def error(self, message):
        """Log error message"""
        self.log(message, "ERROR")
    
    def warning(self, message):
        """Log warning message"""
        self.log(message, "WARNING")

class PerformanceProfiler:
    """Performance profiling utility for comparing algorithms"""
    
    def __init__(self):
        self.results = []
    
    def profile_algorithm(self, algorithm_func, maze, algorithm_name):
        """Profile a single algorithm"""
        timer = Timer()
        timer.start()
        
        result = algorithm_func()
        
        timer.stop()
        
        profile_data = {
            'algorithm': algorithm_name,
            'execution_time': timer.elapsed(),
            'path_found': result is not None,
            'path_length': len(result) if result else 0,
            'maze_size': f"{maze.rows}x{maze.cols}"
        }
        
        self.results.append(profile_data)
        return profile_data
    
    def compare_algorithms(self, algorithms_dict, maze):
        """Compare multiple algorithms on the same maze"""
        comparison_results = []
        
        for name, algorithm_func in algorithms_dict.items():
            result = self.profile_algorithm(algorithm_func, maze, name)
            comparison_results.append(result)
        
        return comparison_results
    
    def get_summary(self):
        """Get summary of all profiling results"""
        if not self.results:
            return "No profiling data available"
        
        summary = "\n" + "="*60
        summary += "\nALGORITHM PERFORMANCE SUMMARY"
        summary += "\n" + "="*60
        
        for result in self.results:
            summary += f"\nAlgorithm: {result['algorithm']}"
            summary += f"\nExecution Time: {result['execution_time']:.4f}s"
            summary += f"\nPath Found: {result['path_found']}"
            summary += f"\nPath Length: {result['path_length']}"
            summary += f"\nMaze Size: {result['maze_size']}"
            summary += "\n" + "-"*40
        
        return summary