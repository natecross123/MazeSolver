# maze_solver.py
# M4 MacBook optimized maze solver - APPLE SILICON COMPATIBLE

import sys
import time
import traceback
import os
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
        self.configure_for_m4()
        self.setup()
    
    def configure_for_m4(self):
        """Configure environment for Computer"""
        try:
            print("Configuring for Computer...")
            
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
            os.environ['PYTHONUNBUFFERED'] = '1'  # Ensure immediate output
            
            # Check Python version and architecture
            print(f"Python version: {sys.version}")
            print(f"Platform: {sys.platform}")
            
            import platform
            if platform.machine() == 'arm64':
                print("✅ Running on Apple Silicon (M-series chip)")
            else:
                print(f"⚠️  Running on {platform.machine()} architecture")
            
            print("M4 MacBook configuration complete")
            
        except Exception as e:
            print(f"Warning during M4 configuration: {e}")
    
    def setup(self):
        """Initialize the maze solver with M4 optimizations"""
        print("Initializing Maze Solver for M4 MacBook...")
        
        try:

            print("Creating maze...")
            self.maze = Maze()

            print("Validating maze...")
            self.maze.validate_maze()
         
            print("Setting up graphics...")
            self.graphics = MazeGraphics(self.maze)
            
            if not self.graphics.setup_successful:
                raise Exception("Graphics setup failed - this should not happen on M4 MacBook")
            
            # Setup algorithms
            print("Setting up algorithms...")
            self.algorithms = SearchAlgorithms(self.maze, self.graphics)
            
            # Setup key bindings
            print("Setting up key bindings...")
            self.graphics.setup_key_bindings(self.handle_key_press)
            
            print("✅ Setup complete!")
            self.display_initial_screen()
            
        except Exception as e:
            print(f"❌ Error during setup: {e}")
            traceback.print_exc()
            print("\nTroubleshooting tips :")
            print("1. Ensure you're using Python 3.9+ with tkinter support")
            print("2. Try: brew install python-tk")
            print("3. Make sure no other turtle graphics programs are running")
            raise
    
    def display_initial_screen(self):
        """Display the initial maze and instructions"""
        try:
            print("Displaying initial screen...")
            self.graphics.refresh_display()
            print("✅ Initial screen displayed successfully")
            
            # Ensure window is focused and ready for input
            if self.graphics.screen:
                try:
                    self.graphics.screen.getcanvas().focus_force()
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Error displaying initial screen: {e}")
            traceback.print_exc()
    
    def handle_key_press(self, action):
        """Handle keyboard input with M4 optimizations"""
        try:
            print(f"🔧 Key pressed: {action}")
            
            if action == 'BFS':
                self.run_search('BFS')
            elif action == 'DFS':
                self.run_search('DFS')
            elif action == 'A*':
                self.run_search('ASTAR')
            elif action == 'RESET':
                self.reset_maze()
            elif action == 'NEW_MAZE':
                self.generate_new_maze()
            elif action == 'SPEED_UP':
                self.graphics.speed_up()
                self.graphics.display_status_message(f"⚡ Speed: {self.graphics.animation_speed:.3f}s", "blue")
                print(f"⚡ Speed increased. Current delay: {self.graphics.animation_speed:.3f}s")
            elif action == 'SLOW_DOWN':
                self.graphics.slow_down()
                self.graphics.display_status_message(f"🐌 Speed: {self.graphics.animation_speed:.3f}s", "blue")
                print(f"🐌 Speed decreased. Current delay: {self.graphics.animation_speed:.3f}s")
            elif action == 'QUIT':
                self.quit_program()
            else:
                print(f"Unknown action: {action}")
                
        except Exception as e:
            print(f"❌ Error handling key press: {e}")
            traceback.print_exc()
    
    def run_search(self, algorithm_name):
        """Run the specified search algorithm with M4 optimizations"""
        try:
            print(f"\n🚀 Running {algorithm_name} algorithm...")
            
            # Clear previous display and update status
            self.graphics.clear_all_text()
            self.graphics.display_title()
            self.graphics.display_maze_info()
            self.graphics.display_instructions()
            self.graphics.display_status_message(f"🔍 Running {algorithm_name}...", "orange")
            
            # Clear previous search results
            self.graphics.clear_search_visualization()
            
            # Run the algorithm with timing
            start_time = time.time()
            path = self.algorithms.run_algorithm(algorithm_name, visualize=True)
            end_time = time.time()
            
            stats = self.algorithms.get_statistics()
            
            # Clear status and display results
            self.graphics.clear_all_text()
            self.graphics.display_title()
            self.graphics.display_maze_info()
            self.graphics.display_instructions()
            
            # Display results
            if path:
                print(f"✅ Path found! Length: {len(path)}")
                self.graphics.draw_path(path)
                self.graphics.display_status_message(
                    f"✅ {stats['algorithm']} found path! Length: {len(path)}", "green")
            else:
                print("❌ No path found!")
                self.graphics.display_status_message(
                    f"❌ {stats['algorithm']}: No path found", "red")
            
            # Display statistics
            self.graphics.display_statistics(stats)
            self.print_statistics(stats)
            
            print(f"🎯 Algorithm completed in {end_time - start_time:.3f} seconds")
            
        except Exception as e:
            print(f"❌ Error running algorithm: {e}")
            traceback.print_exc()
            try:
                self.graphics.display_status_message(f"❌ Error: {str(e)}", "red")
            except:
                pass
    
    def print_statistics(self, stats):
        """Print statistics to console with nice formatting"""
        print("\n" + "="*60)
        print(f"📊 ALGORITHM PERFORMANCE REPORT")
        print("="*60)
        print(f"🔧 Algorithm: {stats['algorithm']}")
        print(f"{'✅' if stats['path_found'] else '❌'} Path found: {stats['path_found']}")
        print(f"🔍 Nodes visited: {stats['nodes_visited']:,}")
        print(f"📏 Path length: {stats['path_length']}")
        print(f"⏱️  Execution time: {stats['time']:.4f} seconds")
        
        if stats['path_found']:
            efficiency = stats['path_length'] / stats['nodes_visited'] if stats['nodes_visited'] > 0 else 0
            print(f"📈 Efficiency: {efficiency:.4f} (path length / nodes visited)")
        
        print("="*60 + "\n")
    
    def reset_maze(self):
        """Reset the maze to initial state"""
        try:
            print("🔄 Resetting maze...")
            self.maze.reset_maze()
            self.graphics.clear_search_visualization()
            self.graphics.refresh_display()
            print("✅ Maze reset successfully")
        except Exception as e:
            print(f"❌ Error resetting maze: {e}")
            traceback.print_exc()
    
    def generate_new_maze(self):
        """Generate a new random maze"""
        try:
            print("🎲 Generating new random maze...")
            
            # Generate new maze
            self.maze.generate_simple_maze()
            
            # Update algorithms with new maze
            self.algorithms.maze = self.maze
            
            # Update graphics with new maze and refresh display
            self.graphics.update_maze(self.maze)
            
            print("✅ New random maze generated!")
            
        except Exception as e:
            print(f"❌ Error generating new maze: {e}")
            traceback.print_exc()
    
    def generate_maze_by_difficulty(self, difficulty):
        """Generate maze by difficulty level"""
        try:
            print(f"🎯 Generating {difficulty} maze...")
            
            # Generate maze with specified difficulty
            self.maze.generate_maze_by_difficulty(difficulty)
            
            # Update algorithms and graphics
            self.algorithms.maze = self.maze
            self.graphics.update_maze(self.maze)
            
            print(f"✅ {difficulty.capitalize()} maze generated!")
            
        except Exception as e:
            print(f"❌ Error generating {difficulty} maze: {e}")
            traceback.print_exc()
    
    def load_predefined_maze(self):
        """Load a predefined interesting maze"""
        try:
            print("📚 Loading predefined maze...")
            
            # Get predefined mazes and pick one randomly
            predefined_mazes = self.maze.get_predefined_mazes()
            maze_name = random.choice(list(predefined_mazes.keys()))
            maze_data = predefined_mazes[maze_name]
            
            # Load the maze
            self.maze.load_from_list(maze_data)
            
            # Update algorithms and graphics
            self.algorithms.maze = self.maze
            self.graphics.update_maze(self.maze)
            
            print(f"✅ Loaded '{maze_name}' maze!")
            
        except Exception as e:
            print(f"❌ Error loading predefined maze: {e}")
            traceback.print_exc()
    
    def quit_program(self):
        """Quit the program safely"""
        print("👋 Quitting maze solver...")
        self.running = False
        try:
            if self.graphics and self.graphics.screen:
                self.graphics.close()
        except Exception as e:
            print(f"Warning during close: {e}")
        
        print("✅ Maze solver terminated successfully")
        sys.exit(0)
    
    def run(self):
        """Main program loop optimized for M4 MacBook"""
        print("\n" + "="*60)
        print("🧩 MAZE SOLVER - RUNNING ON M4 MACBOOK")
        print("="*60)
        print("🎮 CONTROLS:")
        print("   1 - BFS Algorithm")
        print("   2 - DFS Algorithm") 
        print("   3 - A* Algorithm")
        print("   R - Reset Maze")
        print("   N - New Maze")
        print("   + - Speed Up")
        print("   - - Slow Down")
        print("   Q - Quit")
        print("="*60)
        print("🖱️  Click on the turtle window to activate keyboard input!")
        print("🚀 Ready to solve mazes!")
        print("="*60 + "\n")
        
        try:
            # Ensure graphics are ready
            if not self.graphics or not self.graphics.setup_successful:
                raise Exception("Graphics not properly initialized")
            
            # Focus the window for input
            self.graphics.screen.listen()
            
            # Set up window close handler
            try:
                canvas = self.graphics.screen.getcanvas()
                root = canvas.winfo_toplevel()
                root.protocol("WM_DELETE_WINDOW", self.quit_program)
                
                # Bring window to front on M4 MacBook
                root.lift()
                root.attributes('-topmost', True)
                root.after_idle(root.attributes, '-topmost', False)
                
            except Exception as e:
                print(f"Warning: Could not set window properties: {e}")
            
            # Start the main event loop
            print("🔄 Starting main event loop...")
            self.graphics.screen.mainloop()
            
        except KeyboardInterrupt:
            print("\n⚠️  Program interrupted by user")
            self.quit_program()
        except Exception as e:
            print(f"❌ An error occurred in main loop: {e}")
            traceback.print_exc()
            print("\nM4 MacBook troubleshooting:")
            print("1. Try closing any other Python/turtle programs")
            print("2. Restart Terminal and try again")
            print("3. Check if Python has proper permissions")
            self.quit_program()

def main():
    """Main function to start the maze solver with M4 MacBook optimizations"""
    print("🚀 Starting Maze Solver for M4 MacBook...")
    
    solver = None
    try:
        # Pre-flight checks for M4 MacBook
        print("🔍 Running pre-flight checks...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("⚠️  Warning: Python 3.8+ recommended for best M4 compatibility")
        
        # Check if running in virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("🐍 Running in virtual environment")
        
        # Test tkinter availability
        try:
            import tkinter as tk
            test_root = tk.Tk()
            test_root.withdraw()
            test_root.destroy()
            print("✅ tkinter test passed")
        except Exception as e:
            print(f"❌ tkinter test failed: {e}")
            print("💡 Try: brew install python-tk")
            raise
        
        print("✅ Pre-flight checks passed")
        
        # Create and run solver
        solver = MazeSolver()
        solver.run()
        
    except KeyboardInterrupt:
        print("\n⚠️  Application interrupted by user")
    except Exception as e:
        print(f"❌ Failed to start maze solver: {e}")
        traceback.print_exc()
        print("\n🔧 M4 MacBook Troubleshooting Guide:")
        print("1. Ensure you have Python 3.8+ with tkinter:")
        print("   brew install python-tk")
        print("2. If using virtual environment, ensure tkinter is available:")
        print("   pip install tk")
        print("3. Close any other turtle graphics programs")
        print("4. Try running with different Python:")
        print("   python3 maze_solver.py")
        print("5. Check system permissions for Python")
    finally:
        if solver:
            try:
                solver.quit_program()
            except:
                pass
        print("👋 Application terminated")

if __name__ == "__main__":
    main()