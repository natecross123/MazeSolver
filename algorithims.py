from collections import deque
import heapq
import time
from config import *

class SearchAlgorithms:
    def __init__(self, maze, graphics):
        self.maze = maze
        self.graphics = graphics
        self.stats = {}