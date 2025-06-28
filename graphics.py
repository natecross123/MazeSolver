# graphics.py
# Turtle graphics setup and visualization functions

import turtle
import time
from config import *

class MazeGraphics:
    def __init__(self, maze):
        self.maze = maze
        self.screen = None
        self.drawer = None
        self.animation_speed = ANIMATION_SPEED
        self.setup_screen()
        self.setup_drawer()
    
    def setup_screen(self):
        """Initialize the turtle screen"""
        self.screen = turtle.Screen()
        self.screen.title(SCREEN_TITLE)
        self.screen.bgcolor('white')
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)  # Turn off animation for faster drawing
        
        # Calculate screen coordinates
        self.screen_width = self.maze.cols * CELL_SIZE
        self.screen_height = self.maze.rows * CELL_SIZE
        
        # Set coordinate system
        self.screen.setworldcoordinates(
            -self.screen_width//2, -self.screen_height//2,
            self.screen_width//2, self.screen_height//2
        )
    
    def setup_drawer(self):
        """Initialize the drawing turtle"""
        self.drawer = turtle.Turtle()
        self.drawer.speed(0)
        self.drawer.shape('square')
        self.drawer.penup()
    
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
        self.screen.tracer(0)  # Turn off animation for faster drawing
        
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
            # Don't overwrite start and goal
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
    
    def display_message(self, message, x=0, y=-250):
        """Display a text message on screen"""
        text_turtle = turtle.Turtle()
        text_turtle.hideturtle()
        text_turtle.penup()
        text_turtle.goto(x, y)
        text_turtle.color('black')
        text_turtle.write(message, align="center", font=("Arial", 14, "normal"))
    
    def display_instructions(self):
        """Display control instructions"""
        instructions = [
            "Controls:",
            "1 - BFS Algorithm",
            "2 - DFS Algorithm", 
            "3 - A* Algorithm",
            "R - Reset",
            "+ - Speed Up",
            "- - Slow Down",
            "Q - Quit"
        ]
        
        y_start = 200
        for i, instruction in enumerate(instructions):
            self.display_message(instruction, x=-350, y=y_start - i*20)
    
    def display_statistics(self, stats):
        """Display search statistics"""
        stat_text = f"Algorithm: {stats.get('algorithm', 'N/A')} | "
        stat_text += f"Nodes Visited: {stats.get('nodes_visited', 0)} | "
        stat_text += f"Path Length: {stats.get('path_length', 0)} | "
        stat_text += f"Time: {stats.get('time', 0):.3f}s"
        
        self.display_message(stat_text, y=-280)
    
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
        for key, action in KEY_BINDINGS.items():
            self.screen.onkey(lambda a=action: key_handler(a), key)
    
    def wait_for_click(self):
        """Wait for mouse click"""
        self.screen.exitonclick()
    
    def close(self):
        """Close the graphics window"""
        if self.screen:
            self.screen.bye()