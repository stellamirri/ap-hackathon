import pyxel
import random_maze
import random


WIDTH = 30
HEIGHT = 30

# Colors
BLACK = 0
WHITE = 7
PINK = 8
DARK_GREEN = 3
LIGHT_GREEN = 11
GRAY = 13

UP, RIGHT, DOWN, LEFT = (0, -1), (1, 0), (0, 1), (-1, 0) 


#maze = random_maze.maze

def draw_maze(maze, source , target = None):
    pyxel.cls(BLACK)
    for (x,y) in maze:
        pyxel.pset(x, y, WHITE)
    for (x, y) in reachable_cells(maze_to_graph(maze), source):
        pyxel.pset(x, y, LIGHT_GREEN)
    x, y = source
    pyxel.pset(x,y, DARK_GREEN)
    if target is not None:
        path = path_from(maze, source)[target]
        for (x,y) in path:
            pyxel.pset(x, y, PINK)

def maze_to_graph(maze):
    vertices = set(maze)
    edges = set()
    weights = {}
    for vertex in vertices:
        x, y = vertex
        for (dx, dy) in [UP, RIGHT, DOWN, LEFT]:
            if (x +dx, y+dy)  in vertices:
                edge = (vertex, (x+dx, y+dy))
                edges.add(edge)
                weights[edge] = 1
    return vertices, edges, weights


def reachable_cells(graph, source):
    vertices, edges, _ = graph
    todo = {source}
    done = set()
    while todo:
        current = todo.pop()
        neighbors = {v for v in vertices if (current, v) in edges}
        for n in neighbors:
            if n not in done:
                todo.add(n)
        done.add(current)
    print(done)
    return done

def path_from(maze, source):
    vertices, edges, weights = maze_to_graph(maze)
    path = {source: [source]}
    todo = {source}
    done = set()
    while todo:
        current = todo.pop()
        neighbors = {v for v in vertices if (current, v) in edges}
        for n in neighbors:
            if n not in done:
                todo.add(n)
            if n not in path.keys():
                path[n] = path[current] + [n]
        done.add(current)
    return path

def new_target(maze, source):
    graph = maze_to_graph(maze)
    cells = reachable_cells(graph, source)
    return random.choice(list(cells))


#print(path_from(maze, (0, 0))[(29, 29)])

#pyxel.init(WIDTH, HEIGHT)
#draw_maze(maze, (0, 0), (29,29))
#pyxel.show()