# graphics.py
# Simple and reliable turtle graphics for M4 MacBook - NO FANCY FEATURES

import turtle
import time
import sys
import os
from config import *

class MazeGraphics:
    def __init__(self, maze):
        self.maze = maze
        self.screen = None
        self.drawer = None
        self.text_turtles = []
        self.animation_speed = ANIMATION_SPEED
        self.setup_successful = False
        
        print("Setting up SIMPLE graphics for clean maze display...")
        self.setup_screen_simple()
        if self.setup_successful:
            self.setup_drawer_simple()
    
    def setup_screen_simple(self):
        """Super simple screen setup that WILL work on M4"""
        try:
            print("Creating turtle screen...")
            
            # Set environment for M4 compatibility
            os.environ['TK_SILENCE_DEPRECATION'] = '1'
            
            # Create screen with MINIMAL setup
            self.screen = turtle.Screen()
            print("✅ Screen created")
            
            # Basic setup only
            self.screen.title("Maze Solver")
            self.screen.bgcolor('white')
            print("✅ Basic setup done")
            
            # Fixed size for clean display
            self.screen.setup(width=1200, height=600)
            print("✅ Window size set")
            
            # Disable animation initially
            self.screen.tracer(0)
            print("✅ Animation disabled")
            
            # Simple coordinate system - maze on left, text on right
            self.screen.setworldcoordinates(-600, -300, 600, 300)
            print("✅ Coordinates set")
            
            # Layout for clean display - maze doesn't cover text
            self.maze_left = -400
            self.maze_right = 100
            self.instructions_x = 150  # Right side for instructions
            self.bottom_y = -250
            self.top_y = 250
            
            print("✅ Screen setup completed successfully")
            self.setup_successful = True
            
        except Exception as e:
            print(f"❌ Error setting up screen: {e}")
            self.setup_successful = False
            raise
    
    def setup_drawer_simple(self):
        """Simple drawing turtle setup"""
        try:
            print("Setting up drawer...")
            
            self.drawer = turtle.Turtle()
            self.drawer.speed(0)
            self.drawer.shape('square')
            self.drawer.penup()
            
            print("✅ Drawer setup completed")
            
        except Exception as e:
            print(f"❌ Error setting up drawer: {e}")
            raise
    
    def clear_all_text(self):
        """Clear all text safely"""
        try:
            for text_turtle in self.text_turtles[:]:
                try:
                    text_turtle.clear()
                except:
                    pass
            self.text_turtles.clear()
        except:
            pass
    
    def create_text_turtle(self):
        """Create text turtle"""
        try:
            text_turtle = turtle.Turtle()
            text_turtle.hideturtle()
            text_turtle.penup()
            text_turtle.speed(0)
            self.text_turtles.append(text_turtle)
            return text_turtle
        except:
            return None
    
    def maze_to_screen_coords(self, row, col):
        """Convert maze coordinates to screen coordinates - clean layout"""
        # Use appropriate cell size for clean display
        cell_size = 20  # Larger cells for better visibility
        
        # Position maze on the left side, away from text
        maze_width = self.maze.cols * cell_size
        maze_height = self.maze.rows * cell_size
        
        # Center the maze on the left side
        start_x = -350  # Fixed position on left
        start_y = maze_height // 2
        
        x = start_x + col * cell_size + cell_size // 2
        y = start_y - row * cell_size - cell_size // 2
        
        return x, y
    
    def draw_cell(self, row, col, color):
        """Draw a single cell - SIMPLE version"""
        try:
            if not self.drawer or not self.setup_successful:
                return
                
            x, y = self.maze_to_screen_coords(row, col)
            self.drawer.goto(x, y)
            self.drawer.color(color)
            self.drawer.stamp()
            
        except Exception as e:
            print(f"Error drawing cell: {e}")
    
    def draw_maze(self):
        """Draw the maze - SIMPLE version"""
        try:
            if not self.setup_successful:
                return
                
            print("Drawing maze...")
            self.screen.tracer(0)
            
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    cell_value = self.maze.get_cell_value(row, col)
                    
                    if cell_value == WALL:
                        self.draw_cell(row, col, 'black')
                    elif cell_value == START:
                        self.draw_cell(row, col, 'green')
                    elif cell_value == GOAL:
                        self.draw_cell(row, col, 'red')
                    else:
                        self.draw_cell(row, col, 'white')
            
            self.screen.update()
            print("✅ Maze drawn")
            
        except Exception as e:
            print(f"Error drawing maze: {e}")
    
    def draw_visited_cell(self, row, col, algorithm='BFS'):
        """Draw visited cell with animation"""
        try:
            if algorithm == 'BFS':
                color = 'lightblue'
            elif algorithm == 'DFS':
                color = 'lightyellow'
            else:  # A*
                color = 'lightcoral'
                
            self.draw_cell(row, col, color)
            self.screen.update()
            time.sleep(self.animation_speed)
            
        except:
            pass
    
    def draw_path(self, path):
        """Draw the solution path"""
        try:
            if not self.setup_successful:
                return
                
            self.screen.tracer(0)
            for row, col in path:
                if (row, col) not in [self.maze.start, self.maze.goal]:
                    self.draw_cell(row, col, 'orange')
            self.screen.update()
            
        except:
            pass
    
    def clear_search_visualization(self):
        """Clear visited cells"""
        try:
            if not self.setup_successful:
                return
                
            self.screen.tracer(0)
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    if self.maze.get_cell_value(row, col) == FREE:
                        self.draw_cell(row, col, 'white')
            self.screen.update()
            
        except:
            pass
    
    def display_title(self):
        """Display title at top"""
        try:
            title_turtle = self.create_text_turtle()
            if title_turtle:
                title_turtle.goto(0, 260)
                title_turtle.color('darkblue')
                title_turtle.write("MAZE SOLVER", align="center", font=("Arial", 18, "bold"))
        except:
            pass
    
    def display_instructions(self):
        """Display instructions on the right side - clean layout"""
        try:
            instructions = [
                "CONTROLS:",
                "",
                "1 - BFS Algorithm",
                "2 - DFS Algorithm", 
                "3 - A* Algorithm",
                "",
                "R - Reset Maze",
                "N - New Maze",
                "+ - Speed Up",
                "- - Slow Down",
                "Q - Quit",
                "",
                "LEGEND:",
                "Green = Start",
                "Red = Goal",
                "Black = Wall",
                "White = Path",
                "",
                "Blue = BFS Visited",
                "Yellow = DFS Visited",
                "Pink = A* Visited",
                "Orange = Solution"
            ]
            
            start_y = 200
            
            for i, instruction in enumerate(instructions):
                if instruction == "":
                    continue
                    
                instr_turtle = self.create_text_turtle()
                if instr_turtle:
                    instr_turtle.goto(self.instructions_x, start_y - i*18)
                    
                    if instruction in ["CONTROLS:", "LEGEND:"]:
                        instr_turtle.color('darkblue')
                        font_style = ("Arial", 12, "bold")
                    else:
                        instr_turtle.color('black')
                        font_style = ("Arial", 10, "normal")
                    
                    instr_turtle.write(instruction, align="left", font=font_style)
                    
        except:
            pass
    
    def display_status_message(self, message, color='black'):
        """Display status message at bottom"""
        try:
            status_turtle = self.create_text_turtle()
            if status_turtle:
                status_turtle.goto(0, -270)
                status_turtle.color(color)
                status_turtle.write(f"Status: {message}", align="center", font=("Arial", 12, "bold"))
        except:
            pass
    
    def display_statistics(self, stats):
        """Display statistics on the right side"""
        try:
            stat_lines = [
                f"RESULTS:",
                f"Algorithm: {stats.get('algorithm', 'N/A')}",
                f"Nodes Visited: {stats.get('nodes_visited', 0)}",
                f"Path Length: {stats.get('path_length', 0)}",
                f"Time: {stats.get('time', 0):.3f} seconds",
                f"Success: {'YES' if stats.get('path_found', False) else 'NO'}"
            ]
            
            start_y = -80
            
            for i, line in enumerate(stat_lines):
                stat_turtle = self.create_text_turtle()
                if stat_turtle:
                    stat_turtle.goto(self.instructions_x, start_y - i*18)
                    
                    if line == "RESULTS:":
                        stat_turtle.color('darkgreen')
                        font_style = ("Arial", 12, "bold")
                    else:
                        stat_turtle.color('darkgreen')
                        font_style = ("Arial", 10, "normal")
                        
                    stat_turtle.write(line, align="left", font=font_style)
                    
        except:
            pass
    
    def display_maze_info(self):
        """Display maze info at top"""
        try:
            info_turtle = self.create_text_turtle()
            if info_turtle:
                info_turtle.goto(0, 220)
                info_turtle.color('green')
                info_turtle.write(f"Maze Size: {self.maze.rows} x {self.maze.cols} | Click window then press keys!", 
                                align="center", font=("Arial", 11, "normal"))
        except:
            pass
    
    def display_message(self, message, x=0, y=None):
        """Display general message"""
        try:
            if y is None:
                y = -300
            msg_turtle = self.create_text_turtle()
            if msg_turtle:
                msg_turtle.goto(x, y)
                msg_turtle.write(message, align="center", font=("Arial", 11, "normal"))
        except:
            pass
    
    def refresh_display(self):
        """Refresh the display"""
        try:
            if not self.setup_successful:
                return
                
            self.clear_all_text()
            self.draw_maze()
            self.display_title()
            self.display_maze_info()
            self.display_instructions()
            self.display_status_message("Ready! Press 1, 2, or 3", "green")
            
        except Exception as e:
            print(f"Error refreshing display: {e}")
    
    def update_maze(self, new_maze):
        """Update to new maze"""
        self.maze = new_maze
        self.refresh_display()
    
    def speed_up(self):
        """Speed up animation"""
        self.animation_speed = max(0.01, self.animation_speed * 0.5)
    
    def slow_down(self):
        """Slow down animation"""
        self.animation_speed = min(1.0, self.animation_speed * 2.0)
    
    def setup_key_bindings(self, key_handler):
        """Setup keyboard bindings - SIMPLE version"""
        try:
            if not self.setup_successful:
                return
                
            print("Setting up key bindings...")
            self.screen.listen()
            
            # Simple key bindings
            self.screen.onkey(lambda: key_handler('BFS'), '1')
            self.screen.onkey(lambda: key_handler('DFS'), '2')
            self.screen.onkey(lambda: key_handler('A*'), '3')
            self.screen.onkey(lambda: key_handler('RESET'), 'r')
            self.screen.onkey(lambda: key_handler('RESET'), 'R')
            self.screen.onkey(lambda: key_handler('NEW_MAZE'), 'n')
            self.screen.onkey(lambda: key_handler('NEW_MAZE'), 'N')
            self.screen.onkey(lambda: key_handler('QUIT'), 'q')
            self.screen.onkey(lambda: key_handler('QUIT'), 'Q')
            self.screen.onkey(lambda: key_handler('SPEED_UP'), 'plus')
            self.screen.onkey(lambda: key_handler('SLOW_DOWN'), 'minus')
            
            print("✅ Key bindings ready")
            
        except Exception as e:
            print(f"Error setting up key bindings: {e}")
    
    def close(self):
        """Close graphics safely"""
        try:
            self.clear_all_text()
            if self.screen:
                self.screen.bye()
        except:
            pass