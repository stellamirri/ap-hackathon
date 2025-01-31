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
MAGENTA = 2
BEIGE = 14
MARRON = 4
YELLOW = 10

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


pause_bloc = [(j, i) for i in range(13, 18) for j in range(12, 14)] + [(j, i) for i in range(13, 18) for j in range(16, 18)]
maze_set = set()
for i in range(HEIGHT):
     for j in range(WIDTH):
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
        startpos2.append((60+i, 20+j))
dims2 = range(20,30)

startpos3 = []
for i in range(10):
    for j in range(10):
        startpos3.append((30+i, 25+j))
dims3 = range(7,20)


walls1, inside1, doors1 = generate_room(startpos1, dims1, 1)
walls2, inside2, doors2 = generate_room(startpos2, dims2, 2)
walls3, inside3, doors3 = generate_room(startpos3, dims3, 3)
mazeee = maze_set - walls1 - walls2 - walls3 

def generate_corridors(source, target):
    try:
        return set(maze.path_from(maze.reachable_cells(maze.maze_to_graph(mazeee), source), source)[target])
    except:
        print("ça ne marche pas")


corridor1 = generate_corridors(list(doors1)[0], list(doors3)[0])   
corridor3 = generate_corridors(list(doors3)[2], list(doors2)[1])  

#Mode avec unelampe ou l'on ne voit pas le reste
torchMode = True

def spawn_new_snape():
    global snape, snape_direction
    x = rd.choice(list(inside1))
    snape = [x[0], x[1]]
    snape_direction = RIGHT

def spawn_argent():
    global argent1
    global argent2
    global argent3
    argent1 = rd.choice(list(inside1))
    argent2 = rd.choice(list(inside2))
    argent3 = rd.choice(list(inside3))


def spawn_life(): 
    global life 
    life = [[k+1,1] for k in range (5)]
    print(f"points de vie :{len(life)}")

def spawn_everything():
    spawn_new_snape()
    spawn_argent()
    spawn_life()

river = set()

def spawn_river():
    global river
    r = rd.randrange(int(WIDTH*1/3),int(WIDTH*2/3))
    river.add((HEIGHT,r))
    river.add((HEIGHT,r+1))
    for i in range(HEIGHT):
        r += rd.randrange(-1,1)
        river.add((HEIGHT-i,r))
        river.add((HEIGHT-i,r+1))

def river_effect():
    global river
    clear = rd.sample(list(river), 50)
    display (5, list(river))
    display (12, clear)


spawn_everything()
spawn_river()
score = 0

arrow_keys = [
    pyxel.KEY_UP, 
    pyxel.KEY_DOWN, 
    pyxel.KEY_LEFT, 
    pyxel.KEY_RIGHT
]

def move_up():
    global snape_direction
    if (snape[0] + UP[0],snape[1] + UP[1]) in list(walls1|walls2|walls3):
        snape_direction = [0,0]
    else : 
        snape_direction = UP
    snape_move()

def move_down():
    global snape_direction
    if (snape[0] + DOWN[0], snape[1] + DOWN[1]) in list(walls1|walls2|walls3):
        snape_direction = [0,0]
    else : 
        snape_direction = DOWN
    snape_move()

def move_left():
    global snape_direction
    if (snape[0] + LEFT[0],snape[1] + LEFT[1]) in list(walls1|walls2|walls3):
        snape_direction = [0,0]
    else : 
        snape_direction = LEFT
    snape_move()

def move_right():
    global snape_direction
    if (snape[0] + RIGHT[0],snape[1] + RIGHT[1])in list(walls1|walls2|walls3):
        snape_direction = [0,0]
    else : 
        snape_direction = RIGHT
    snape_move()


p = False

def pause():
    global p
    if p:
         p = False
    else:
         p = True


def crash(new_snake_head):
    if (
        (
        new_snake_head[0] < 0
        or new_snake_head[0] > HEIGHT -1
        or new_snake_head[1] < 0
        or new_snake_head[1] > WIDTH -1
        or tuple(new_snake_head) in mazeee - inside1 - inside2 - inside3 - doors1 -doors2 - doors3 - corridor1 - corridor3
        )
    ):
        return True
    return False

def lampe(snape, snape_direction):
    if torchMode:
        eclair = set()
        for i in range (1,6):
            for j in range (1,6):
                if [snape[0]+i-3, snape[1]+j-3] != snape : 
                    eclair.add((snape[0]+i-3, snape[1]+j-3))
        return eclair

def game_over():
    #clear screen 0=noir, palette par défaut avec 16 couleurs adressée par un entier de 0 à 15
    color = pyxel.frame_count % 16 # le clignotement par couleur est calculé en faisant le nb de frame modulo 15 (nb de couleurs disponibles sur la palette)
    pyxel.cls(color)
    pyxel.text(HEIGHT//2-25,WIDTH//2,  "Game over ..", 0)#


def snape_move():
    global snape, snape_direction
    snape = [snape[0]+snape_direction[0], snape[1]+snape_direction[1]]
    if p:
        return None
    if crash(snape):
        if len(life) == 0:
            pyxel.run(update, game_over)
        life.pop()
        print(f"points de vie :{len(life)}")
    elif snape in [argent1 or argent2 or argent3]:
        score +=1
        spawn_everything()
    

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
    display(LIGHT_GREEN)
    if p:
         display(GRAY, pause_bloc)  
    

    display(PINK, life)
    river_effect()
    display (MARRON, list(walls1|walls2|walls3))
    display(BEIGE, list(inside1|inside2|inside3))
    display(12, list(doors1|doors2|doors3))
    display(MAGENTA, [snape])
    if torchMode:
        display(BLACK, maze_set - lampe(snape, snape_direction))

events.register(pyxel.KEY_Q, pyxel.quit)
events.register(pyxel.KEY_UP, move_up)
events.register(pyxel.KEY_DOWN, move_down)
events.register(pyxel.KEY_LEFT, move_left)
events.register(pyxel.KEY_RIGHT, move_right)
events.register(pyxel.KEY_P, pause)


pyxel.run(update, draw)


