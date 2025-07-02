# algorithms.py
# Implementation of BFS, DFS, and A* search algorithms

from collections import deque
import heapq
import time
from config import *

class SearchAlgorithms:
    def __init__(self, maze, graphics):
        self.maze = maze
        self.graphics = graphics
        self.stats = {}
    
    def reconstruct_path(self, parent, start, goal):
        """Reconstruct path from goal to start using parent pointers"""
        path = []
        current = goal
        
        while current is not None:
            path.append(current)
            current = parent.get(current)
        
        path.reverse()
        return path
    
    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance heuristic"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def bfs(self, visualize=True):
        """Breadth-First Search implementation"""
        start_time = time.time()
        start = self.maze.start
        goal = self.maze.goal
        
        # Initialize data structures
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        nodes_visited = 0
        
        while queue:
            current = queue.popleft()
            nodes_visited += 1
            
            # Visualize current node (except start)
            if visualize and current != start:
                self.graphics.draw_visited_cell(current[0], current[1], 'BFS')
            
            # Check if goal reached
            if current == goal:
                path = self.reconstruct_path(parent, start, goal)
                end_time = time.time()
                
                self.stats = {
                    'algorithm': 'BFS',
                    'nodes_visited': nodes_visited,
                    'path_length': len(path),
                    'time': end_time - start_time,
                    'path_found': True
                }
                
                return path
            
            # Explore neighbors
            for neighbor in self.maze.get_neighbors(current[0], current[1]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        # No path found
        end_time = time.time()
        self.stats = {
            'algorithm': 'BFS',
            'nodes_visited': nodes_visited,
            'path_length': 0,
            'time': end_time - start_time,
            'path_found': False
        }
        
        return None
    
    def dfs(self, visualize=True):
        """Depth-First Search implementation"""
        start_time = time.time()
        start = self.maze.start
        goal = self.maze.goal
        
        # Initialize data structures
        stack = [start]
        visited = {start}
        parent = {start: None}
        nodes_visited = 0
        
        while stack:
            current = stack.pop()
            nodes_visited += 1
            
            # Visualize current node (except start)
            if visualize and current != start:
                self.graphics.draw_visited_cell(current[0], current[1], 'DFS')
            
            # Check if goal reached
            if current == goal:
                path = self.reconstruct_path(parent, start, goal)
                end_time = time.time()
                
                self.stats = {
                    'algorithm': 'DFS',
                    'nodes_visited': nodes_visited,
                    'path_length': len(path),
                    'time': end_time - start_time,
                    'path_found': True
                }
                
                return path
            
            # Explore neighbors (reverse order for consistent behavior)
            neighbors = self.maze.get_neighbors(current[0], current[1])
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    stack.append(neighbor)
        
        # No path found
        end_time = time.time()
        self.stats = {
            'algorithm': 'DFS',
            'nodes_visited': nodes_visited,
            'path_length': 0,
            'time': end_time - start_time,
            'path_found': False
        }
        
        return None
    
    def astar(self, visualize=True):
        """A* Search implementation"""
        start_time = time.time()
        start = self.maze.start
        goal = self.maze.goal
        
        # Initialize data structures
        open_set = [(0, start)]  # (f_score, node)
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, goal)}
        visited = set()
        nodes_visited = 0
        
        while open_set:
            # Get node with lowest f_score
            current_f, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
                
            visited.add(current)
            nodes_visited += 1
            
            # Visualize current node (except start)
            if visualize and current != start:
                self.graphics.draw_visited_cell(current[0], current[1], 'ASTAR')
            
            # Check if goal reached
            if current == goal:
                path = self.reconstruct_path(came_from, start, goal)
                end_time = time.time()
                
                self.stats = {
                    'algorithm': 'A*',
                    'nodes_visited': nodes_visited,
                    'path_length': len(path),
                    'time': end_time - start_time,
                    'path_found': True
                }
                
                return path
            
            # Explore neighbors
            for neighbor in self.maze.get_neighbors(current[0], current[1]):
                if neighbor in visited:
                    continue
                
                # Calculate tentative g_score
                tentative_g = g_score[current] + 1
                
                # If this path to neighbor is better than previously recorded
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # No path found
        end_time = time.time()
        self.stats = {
            'algorithm': 'A*',
            'nodes_visited': nodes_visited,
            'path_length': 0,
            'time': end_time - start_time,
            'path_found': False
        }
        
        return None
    
    def run_algorithm(self, algorithm_name, visualize=True):
        """Run the specified algorithm"""
        algorithm_name = algorithm_name.upper()
        
        if algorithm_name == 'BFS':
            return self.bfs(visualize)
        elif algorithm_name == 'DFS':
            return self.dfs(visualize)
        elif algorithm_name in ['ASTAR', 'A*']:
            return self.astar(visualize)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    def get_statistics(self):
        """Get the latest search statistics"""
        return self.stats.copy()