# maze_solver.py
# Main program controller for the maze solver

import sys
import time
from maze import Maze
from graphics import MazeGraphics
from algorithms import SearchAlgorithms
from config import *

class MazeSolver:
    def __init__(self):
        self.maze = None
        self.graphics = None
        self.algorithms = None
        self.current_algorithm = None
        self.running = True
        self.setup()
    
    def setup(self):
        """Initialize the maze solver"""
        print("Initializing Maze Solver...")
        
        # Create maze
        self.maze = Maze()
        
        # Optionally load a sample maze for testing
        # sample_maze = self.maze.get_sample_maze()
        # self.maze.load_from_list(sample_maze)
        
        # Validate maze
        self.maze.validate_maze()
        
        # Setup graphics
        self.graphics = MazeGraphics(self.maze)
        
        # Setup algorithms
        self.algorithms = SearchAlgorithms(self.maze, self.graphics)
        
        # Setup key bindings
        self.graphics.setup_key_bindings(self.handle_key_press)
        
        print("Setup complete!")
        self.display_initial_screen()
    
    def display_initial_screen(self):
        """Display the initial maze and instructions"""
        self.graphics.draw_maze()
        self.graphics.display_instructions()
        self.graphics.display_message(
            "Select an algorithm: 1=BFS, 2=DFS, 3=A*", 
            y=-200
        )
    
    def handle_key_press(self, action):
        """Handle keyboard input"""
        if action == 'BFS':
            self.run_search('BFS')
        elif action == 'DFS':
            self.run_search('DFS')
        elif action == 'A*':
            self.run_search('ASTAR')
        elif action == 'RESET':
            self.reset_maze()
        elif action == 'SPEED_UP':
            self.graphics.speed_up()
            print(f"Speed increased. Current delay: {self.graphics.animation_speed:.3f}s")
        elif action == 'SLOW_DOWN':
            self.graphics.slow_down()
            print(f"Speed decreased. Current delay: {self.graphics.animation_speed:.3f}s")
        elif action == 'QUIT':
            self.quit_program()
    
    def run_search(self, algorithm_name):
        """Run the specified search algorithm"""
        print(f"Running {algorithm_name} algorithm...")
        
        # Clear previous search results
        self.graphics.clear_search_visualization()
        
        # Run the algorithm
        try:
            path = self.algorithms.run_algorithm(algorithm_name, visualize=True)
            stats = self.algorithms.get_statistics()
            
            # Display results
            if path:
                print(f"Path found! Length: {len(path)}")
                self.graphics.draw_path(path)
                self.display_success_message(stats)
            else:
                print("No path found!")
                self.display_failure_message(stats)
            
            # Display statistics
            self.graphics.display_statistics(stats)
            self.print_statistics(stats)
            
        except Exception as e:
            print(f"Error running algorithm: {e}")
            self.graphics.display_message(f"Error: {str(e)}", y=-200)
    
    def display_success_message(self, stats):
        """Display success message"""
        message = f"Path found using {stats['algorithm']}!"
        self.graphics.display_message(message, y=-230, x=0)
    
    def display_failure_message(self, stats):
        """Display failure message"""
        message = f"No path found using {stats['algorithm']}"
        self.graphics.display_message(message, y=-230, x=0)
    
    def print_statistics(self, stats):
        """Print statistics to console"""
        print("\n" + "="*50)
        print(f"Algorithm: {stats['algorithm']}")
        print(f"Path found: {stats['path_found']}")
        print(f"Nodes visited: {stats['nodes_visited']}")
        print(f"Path length: {stats['path_length']}")
        print(f"Execution time: {stats['time']:.4f} seconds")
        print("="*50 + "\n")
    
    def reset_maze(self):
        """Reset the maze to initial state"""
        print("Resetting maze...")
        self.maze.reset_maze()
        self.graphics.clear_search_visualization()
        self.graphics.draw_maze()
        self.graphics.display_message(
            "Maze reset. Select an algorithm: 1=BFS, 2=DFS, 3=A*", 
            y=-200
        )
    
    def generate_new_maze(self):
        """Generate a new random maze"""
        print("Generating new maze...")
        self.maze.generate_maze()
        self.graphics.draw_maze()
        self.graphics.display_message(
            "New maze generated. Select an algorithm: 1=BFS, 2=DFS, 3=A*", 
            y=-200
        )
    
    def quit_program(self):
        """Quit the program"""
        print("Quitting maze solver...")
        self.running = False
        self.graphics.close()
        sys.exit(0)
    
    def run(self):
        """Main program loop"""
        print("Maze Solver started!")
        print("Use keyboard controls to interact:")
        print("1 - BFS, 2 - DFS, 3 - A*")
        print("R - Reset, + - Speed up, - - Slow down, Q - Quit")
        
        try:
            # Keep the program running
            while self.running:
                self.graphics.screen.update()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.quit_program()

def main():
    """Main function to start the maze solver"""
    try:
        solver = MazeSolver()
        solver.run()
    except Exception as e:
        print(f"Failed to start maze solver: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()