import pyxel
import events
import random_maze
import maze
import numpy as np
import random as rd

# Geometry
WIDTH = 60
HEIGHT = 110

# Frame rate
FPS = 10

# Colors
BLACK = 0
WHITE = 7
PINK = 8
DARK_GREEN = 3
LIGHT_GREEN = 11
GRAY = 13

# Directions
UP = [0, -1]
RIGHT = [1, 0]
DOWN = [0, 1]
LEFT = [-1, 0]

ARROW_KEYS = [
    pyxel.KEY_UP, 
    pyxel.KEY_DOWN, 
    pyxel.KEY_LEFT, 
    pyxel.KEY_RIGHT
]

pyxel.init(HEIGHT, WIDTH, fps=10)

snake_geometry = [
    [30, 60],
]

snake_direction = RIGHT


rocks_set = set()

pause_bloc = [(j, i) for i in range(13, 18) for j in range(12, 14)] + [(j, i) for i in range(13, 18) for j in range(16, 18)]
maze_set = set()
for i in range(WIDTH):
     for j in range(HEIGHT):
          maze_set.add((i,j))

def list_to_set(list):
    new_set = set()
    for k in list:
        if type(k) == type(list):
            new_tuple = tuple()
            for i in k:
                new_tuple += (i,)
        new_set.add(new_tuple)
    return new_set


def generate_room(startpos, dims, doornumber): #startpos = zone pour le haut gauche de la piece, #dims = liste de taille de cote possible
    start = rd.choice(startpos)
    size = (rd.choice(dims), rd.choice(dims))
    walls = set()
    inside = set()
    doors = set()
    for i in range(size[0]):
        for j in range(size[1]):
            walls.add((start[0]+i, start[1]+j))
    for i in range(1,size[0]-1):
        for j in range(1,size[1]-1):
            inside.add((start[0]+i, start[1]+j))
    walls = walls-inside        
    for i in range(doornumber):
        doors.add(rd.choice(list(walls)))
        walls = walls-doors

    return walls, inside, doors


#PARAMETRES DES SALLES
startpos1 = []
for i in range(10):
    for j in range(10):
        startpos1.append((7+i, 5+j))
dims1 = range(7,30)

startpos2 = []
for i in range(10):
    for j in range(10):
        startpos2.append((50+i, 10+j))
dims2 = range(20,40)

startpos3 = []
for i in range(10):
    for j in range(10):
        startpos3.append((30+i, 25+j))
dims3 = range(7,20)

#######################

walls1, inside1, doors1 = generate_room(startpos1, dims1, 1)
walls2, inside2, doors2 = generate_room(startpos2, dims2, 2)
walls3, inside3, doors3 = generate_room(startpos3, dims3, 3)

# def spawn_room (walls, inside, doors): 
#     global walls1, inside1, doors1
#     walls1, inside1, doors1 = generate_room(startpos1, dims1, 2)
#     print(walls1, inside1, doors1)



"""def spawn_new_rocks():
    global rocks
    rocks = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if (i+j) % 5 == 0 and (i-j) % 11 == 0:
                rocks.append([i, j])
                rocks_set.add((i, j))
"""
def spawn_new_snake():
    global snake_geometry, snake_direction
    snake_geometry = [
        [10, 15],
    ]
    snake_direction = RIGHT

def spawn_new_fruit():
    global fruit
    while True:
        fruit = [pyxel.rndi(0, WIDTH-1), pyxel.rndi(0, HEIGHT-1)]
        if fruit not in snake_geometry and fruit:
            break

def spawn_life(): 
    global life 
    life = [[k+1,1] for k in range (5)]
    print(f"points de vie :{len(life)}")

def spawn_everything():
    #spawn_new_rocks()
    #spawn_new_snake()
    spawn_new_fruit()
# spawn_room()
spawn_life()
spawn_new_snake()
spawn_everything()

score = 0
maze_set = maze_set - rocks_set 

arrow_keys = [
    pyxel.KEY_UP, 
    pyxel.KEY_DOWN, 
    pyxel.KEY_LEFT, 
    pyxel.KEY_RIGHT
]

def move_up():
    global snake_direction
    if snake_direction != DOWN:
            snake_direction = UP
    snake_move()

def move_down():
    global snake_direction
    if snake_direction != UP:
            snake_direction = DOWN
    snake_move()

def move_left():
    global snake_direction
    if snake_direction != RIGHT:
            snake_direction = LEFT
    snake_move()

def move_right():
    global snake_direction
    if snake_direction != LEFT:
            snake_direction = RIGHT
    snake_move()


p = False

def pause():
    global p
    if p:
         p = False
    else:
         p = True

def bang_walls(snake_head):
    if snake_head in list(walls1): 
        return True
    return False

def crash(new_snake_head):
    global snake_geometry, snake_direction, rocks
    if (
        new_snake_head in snake_geometry
        or (
        new_snake_head[0] < 0
        or new_snake_head[0] > HEIGHT -1
        or new_snake_head[1] < 0
        or new_snake_head[1] > WIDTH -1
        )
    ):
        return True
    return False

def game_over():
     #clear screen 0=noir, palette par défaut avec 16 couleurs adressée par un entier de 0 à 15
    color = pyxel.frame_count % 16 # le clignotement par couleur est calculé en faisant le nb de frame modulo 15 (nb de couleurs disponibles sur la palette)
    pyxel.cls(color)
    pyxel.text(HEIGHT//2-25,WIDTH//2,  "Game over ..", 0)#



def snake_move():
    global snake_geometry, snake_direction
    snake_head = snake_geometry[-1]
    if bang_walls([
        snake_head[0] + snake_direction[0],
        snake_head[1] + snake_direction[1],
    ]): 
        new_snake_head = snake_head
    else : 
        new_snake_head = [
            snake_head[0] + snake_direction[0],
            snake_head[1] + snake_direction[1],
        ]
    if p:
        return None
    
    if crash(new_snake_head):
        if len(life) == 0:
            pyxel.run(update, game_over)
        life.pop()
        print(f"points de vie :{len(life)}")
    elif new_snake_head == fruit:
        snake_geometry = snake_geometry + [new_snake_head]
        spawn_everything()
    else:
        snake_geometry = snake_geometry[1:] + [new_snake_head]
    



def update():
    global maze_set, snake_geometry
    events.handle()
    #snake_move()

def display(color, position = None):
    if position == None:
        pyxel.cls(color)
        return None
    for x, y in position:
        pyxel.pset(x, y, color)

def draw():
    display(WHITE)
    snake_body = snake_geometry[:-1]
    snake_head = snake_geometry[-1]

    if p:
         display(GRAY, pause_bloc)  
    
    display(PINK, [fruit])
    display(PINK, life)
    display (BLACK, list(walls1|walls2|walls3))
    display(GRAY, list(inside1|inside2|inside3))
    display(12, list(doors1|doors2|doors3))
    display(DARK_GREEN, snake_body)
    display(LIGHT_GREEN, [snake_head])

events.register(pyxel.KEY_Q, pyxel.quit)
events.register(pyxel.KEY_UP, move_up)
events.register(pyxel.KEY_DOWN, move_down)
events.register(pyxel.KEY_LEFT, move_left)
events.register(pyxel.KEY_RIGHT, move_right)
events.register(pyxel.KEY_P, pause)


pyxel.run(update, draw)