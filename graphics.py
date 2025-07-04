# graphics.py
# Turtle graphics setup and visualization functions - IMPROVED VERSION

import turtle
import time
from config import *

class MazeGraphics:
    def __init__(self, maze):
        self.maze = maze
        self.screen = None
        self.drawer = None
        self.text_turtles = []  # Track all text turtles to clear them
        self.animation_speed = ANIMATION_SPEED
        self.setup_screen()
        self.setup_drawer()
    
    def setup_screen(self):
        """Initialize the turtle screen with proper layout"""
        self.screen = turtle.Screen()
        self.screen.title(SCREEN_TITLE)
        self.screen.bgcolor('white')
        
        # Dynamic window size based on maze size
        maze_width = self.maze.cols * CELL_SIZE
        maze_height = self.maze.rows * CELL_SIZE
        
        # Add padding for UI elements
        total_width = maze_width + 400  # Space for instructions
        total_height = maze_height + 300  # Space for messages
        
        self.screen.setup(width=total_width, height=total_height)
        self.screen.tracer(0)
        
        # Set coordinate system
        self.screen.setworldcoordinates(
            -(total_width//2), -(total_height//2),
            total_width//2, total_height//2
        )
        
        # Store layout boundaries
        self.maze_left = -(maze_width//2)
        self.maze_right = maze_width//2
        self.instructions_x = self.maze_right + 30
        self.bottom_y = -(total_height//2) + 50
        self.top_y = total_height//2 - 50
    
    def setup_drawer(self):
        """Initialize the drawing turtle"""
        self.drawer = turtle.Turtle()
        self.drawer.speed(0)
        self.drawer.shape('square')
        self.drawer.penup()
    
    def clear_all_text(self):
        """Clear all text from screen"""
        for text_turtle in self.text_turtles:
            try:
                text_turtle.clear()
            except:
                pass
        self.text_turtles.clear()
    
    def create_text_turtle(self):
        """Create a new text turtle and track it"""
        text_turtle = turtle.Turtle()
        text_turtle.hideturtle()
        text_turtle.penup()
        text_turtle.speed(0)
        self.text_turtles.append(text_turtle)
        return text_turtle
    
    def maze_to_screen_coords(self, row, col):
        """Convert maze coordinates to screen coordinates"""
        x = (col - self.maze.cols // 2) * CELL_SIZE + CELL_SIZE // 2
        y = (self.maze.rows // 2 - row) * CELL_SIZE - CELL_SIZE // 2
        return x, y
    
    def draw_cell(self, row, col, color, size=CELL_SIZE):
        """Draw a single cell at the specified position"""
        x, y = self.maze_to_screen_coords(row, col)
        self.drawer.goto(x, y)
        self.drawer.color(color)
        self.drawer.stamp()
    
    def draw_maze(self):
        """Draw the complete maze"""
        self.screen.tracer(0)
        
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                cell_value = self.maze.get_cell_value(row, col)
                
                if cell_value == WALL:
                    self.draw_cell(row, col, COLORS['WALL'])
                elif cell_value == START:
                    self.draw_cell(row, col, COLORS['START'])
                elif cell_value == GOAL:
                    self.draw_cell(row, col, COLORS['GOAL'])
                else:  # FREE space
                    self.draw_cell(row, col, COLORS['FREE'])
        
        self.screen.update()
    
    def draw_visited_cell(self, row, col, algorithm='BFS'):
        """Draw a visited cell with algorithm-specific color"""
        color_key = f'VISITED_{algorithm.upper()}'
        color = COLORS.get(color_key, COLORS['VISITED_BFS'])
        self.draw_cell(row, col, color)
        self.screen.update()
        time.sleep(self.animation_speed)
    
    def draw_path(self, path):
        """Draw the final path"""
        self.screen.tracer(0)
        for row, col in path:
            if (row, col) not in [self.maze.start, self.maze.goal]:
                self.draw_cell(row, col, COLORS['PATH'])
        self.screen.update()
    
    def clear_search_visualization(self):
        """Clear visited cells but keep maze structure"""
        self.screen.tracer(0)
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                cell_value = self.maze.get_cell_value(row, col)
                if cell_value == FREE:
                    self.draw_cell(row, col, COLORS['FREE'])
        self.screen.update()
    
    def display_title(self):
        """Display title at top"""
        title_turtle = self.create_text_turtle()
        title_turtle.goto(0, self.top_y)
        title_turtle.color('darkblue')
        title_turtle.write("🧩 MAZE SOLVER - BFS, DFS, A*", align="center", font=("Arial", 16, "bold"))
    
    def display_instructions(self):
        """Display control instructions on the right side"""
        instructions = [
            "🎮 CONTROLS:",
            "",
            "1 - BFS Algorithm",
            "2 - DFS Algorithm", 
            "3 - A* Algorithm",
            "R - Reset Maze",
            "N - New Maze",
            "+ - Speed Up",
            "- - Slow Down",
            "Q - Quit",
            "",
            "📊 LEGEND:",
            "🟩 Start Position",
            "🟥 Goal Position", 
            "⬛ Wall",
            "⬜ Free Space",
            "🟦 BFS Visited",
            "🟡 DFS Visited",
            "🟫 A* Visited",
            "🟧 Solution Path"
        ]
        
        start_y = self.top_y - 50
        
        for i, instruction in enumerate(instructions):
            instr_turtle = self.create_text_turtle()
            instr_turtle.goto(self.instructions_x, start_y - i*20)
            
            if instruction.startswith(('🎮', '📊')):
                instr_turtle.color('darkblue')
                font_style = ("Arial", 11, "bold")
            elif instruction == "":
                continue
            else:
                instr_turtle.color('black')
                font_style = ("Arial", 9, "normal")
            
            instr_turtle.write(instruction, align="left", font=font_style)
    
    def display_status_message(self, message, color='black'):
        """Display status message at designated area"""
        # Create dedicated status turtle
        status_turtle = self.create_text_turtle()
        status_turtle.goto(0, self.bottom_y + 80)
        status_turtle.color(color)
        status_turtle.write(f"Status: {message}", align="center", font=("Arial", 12, "bold"))
    
    def display_statistics(self, stats):
        """Display search statistics"""
        stat_lines = [
            f"Algorithm: {stats.get('algorithm', 'N/A')}",
            f"Nodes Visited: {stats.get('nodes_visited', 0)}",
            f"Path Length: {stats.get('path_length', 0)}",
            f"Execution Time: {stats.get('time', 0):.3f}s",
            f"Success: {'✅ Yes' if stats.get('path_found', False) else '❌ No'}"
        ]
        
        stats_start_y = self.bottom_y + 40
        
        for i, line in enumerate(stat_lines):
            stat_turtle = self.create_text_turtle()
            stat_turtle.goto(0, stats_start_y - i*15)
            stat_turtle.color('purple')
            stat_turtle.write(line, align="center", font=("Arial", 10, "normal"))
    
    def display_maze_info(self):
        """Display current maze information"""
        info_turtle = self.create_text_turtle()
        info_turtle.goto(0, self.top_y - 30)
        info_turtle.color('green')
        maze_info = f"Maze Size: {self.maze.rows}x{self.maze.cols} | Click window then press keys!"
        info_turtle.write(maze_info, align="center", font=("Arial", 11, "normal"))
    
    def display_message(self, message, x=0, y=None):
        """Display a general message"""
        if y is None:
            y = self.bottom_y
        
        msg_turtle = self.create_text_turtle()
        msg_turtle.goto(x, y)
        msg_turtle.color('black')
        msg_turtle.write(message, align="center", font=("Arial", 11, "normal"))
    
    def refresh_display(self):
        """Refresh the entire display with clean layout"""
        # Clear all text first
        self.clear_all_text()
        
        # Redraw maze
        self.draw_maze()
        
        # Redraw UI elements in order
        self.display_title()
        self.display_maze_info()
        self.display_instructions()
        self.display_status_message("Ready! Press 1, 2, or 3 to start", "green")
        
        self.screen.update()
    
    def update_maze(self, new_maze):
        """Update to a new maze and refresh display"""
        self.maze = new_maze
        
        # Recalculate layout for new maze size
        maze_width = self.maze.cols * CELL_SIZE
        maze_height = self.maze.rows * CELL_SIZE
        total_width = maze_width + 400
        total_height = maze_height + 300
        
        # Update screen size if needed
        self.screen.setup(width=total_width, height=total_height)
        self.screen.setworldcoordinates(
            -(total_width//2), -(total_height//2),
            total_width//2, total_height//2
        )
        
        # Update layout boundaries
        self.maze_right = maze_width//2
        self.instructions_x = self.maze_right + 30
        self.bottom_y = -(total_height//2) + 50
        self.top_y = total_height//2 - 50
        
        # Refresh display
        self.refresh_display()
    
    def set_animation_speed(self, speed):
        """Set the animation speed"""
        self.animation_speed = max(0.01, min(1.0, speed))
    
    def speed_up(self):
        """Increase animation speed"""
        self.animation_speed = max(0.01, self.animation_speed * 0.5)
    
    def slow_down(self):
        """Decrease animation speed"""
        self.animation_speed = min(1.0, self.animation_speed * 2.0)
    
    def setup_key_bindings(self, key_handler):
        """Setup keyboard event handlers"""
        self.screen.listen()
        
        # Enhanced key bindings with new maze option
        enhanced_bindings = KEY_BINDINGS.copy()
        enhanced_bindings['n'] = 'NEW_MAZE'
        
        for key, action in enhanced_bindings.items():
            self.screen.onkey(lambda a=action: key_handler(a), key)
    
    def wait_for_click(self):
        """Wait for mouse click"""
        self.screen.exitonclick()
    
    def close(self):
        """Close the graphics window"""
        self.clear_all_text()
        if self.screen:
            self.screen.bye()