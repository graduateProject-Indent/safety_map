import hexgrid
import heapq
import collections
from typing import TypeVar,Tuple,Iterator,Dict,List
import math
import numpy as np
from queue import PriorityQueue
Location = TypeVar('Location')
GridLocation = Tuple[int, int]
Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
Point = collections.namedtuple("Point", ["x", "y"])
#Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])

layout_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
layout_flat = Orientation(3.0 / 2.0, 0.0, math.sqrt(3.0) / 2.0, math.sqrt(3.0), 2.0 / 3.0, 0.0, -1.0 / 3.0, math.sqrt(3.0) / 3.0, 0.0)


rate = 110.574 / (111.320 * math.cos(37.550396 * math.pi / 180))
class HexGrid:
    def __init__(self,orientation: Orientation , size: Point, origin: Point,radius :int):
        self.orientation=orientation
        self.size=size
        self.origin=origin
        self.radius = radius
        self.walls: List[GridLocation] = []
        self.road: List[GridLocation]=[]
    def hex_to_pixel(self,h):
        M = self.orientation
        size = self.size
        origin =self.origin
        x = (M.f0 * h.q + M.f1 * h.r) * size.x
        y = (M.f2 * h.q + M.f3 * h.r) * size.y
        return Point(x + origin.x, y + origin.y)
    def pixel_to_hex(self,p):
        M = self.orientation
        size = self.size
        origin =self.origin
        pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
        q = M.b0 * pt.x + M.b1 * pt.y
        r = M.b2 * pt.x + M.b3 * pt.y
        return hexgrid.Hex(q,r)
    
    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return -self.radius<= x < self.radius and -self.radius<= y < self.radius
    
    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x+1, y-1), (x, y-1), (x-1, y),(x-1,y+1),(x,y+1)]
        if (x + y) % 2 == 0: neighbors.reverse() # aesthetics
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results
class WeightedGraph(HexGrid):
    def cost(self, from_id: Location, to_id: Location) -> float: pass

class GridWithWeights(HexGrid):
    def __init__(self, orientation: Orientation , size: Point, origin: Point,radius: int):
        super().__init__(orientation,size,origin,radius)
        self.weights: Dict[GridLocation, float] = {}
    
    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node,200)

def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:
        path.append(current)
        current = came_from[current]
       
    path.append(start) # optional
    path.reverse() # optional
    return path

def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = dx - dy
    return 200 * max(abs(dx), abs(dy))

def a_star_search(graph:GridWithWeights, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal:
            break
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + int(graph.cost(current, next))
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
                
    
    return came_from, cost_so_far





