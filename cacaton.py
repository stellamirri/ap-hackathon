import pyxel
import events
import random_maze
import maze

class Monster():
    def __init__(self, place, power = 100, pv = 100):
        self.pv = pv
        self.power = power
        self.place = place
        self.target = False

    def move():
        pass

    def attack():
        pass


# Geometry
WIDTH = 30
HEIGHT = 30

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
    [10, 15],
    [11, 15],
    [12, 15],
]

snake_direction = RIGHT


rocks_set = set()

pause_bloc = [(j, i) for i in range(13, 18) for j in range(12, 14)] + [(j, i) for i in range(13, 18) for j in range(16, 18)]
maze_set = set()
for i in range(30):
     for j in range(30):
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

monsters_loc = []
monsters = {}
monster = []
def spawn_monsters():
    global monsters_loc
    global monster
    while True:
        loc = [pyxel.rndi(0, WIDTH-1), pyxel.rndi(0, HEIGHT-1)]
        if loc not in snake_geometry and loc not in rocks:
            break
    monsters[0] = Monster(loc)
    monsters_loc.append(loc)



def spawn_new_rocks():
    global rocks
    rocks = []
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if (i+j) % 5 == 0 and (i-j) % 11 == 0:
                rocks.append([i, j])
                rocks_set.add((i, j))

def spawn_new_snake():
    global snake_geometry, snake_direction
    snake_geometry = [
        [10, 15],
        [11, 15],
        [12, 15],
    ]
    snake_direction = RIGHT

def spawn_new_fruit():
    global fruit
    while True:
        fruit = [pyxel.rndi(0, WIDTH-1), pyxel.rndi(0, HEIGHT-1)]
        if fruit not in snake_geometry and fruit not in rocks:
            break

def spawn_everything():
    spawn_new_rocks()
    #spawn_new_snake()
    spawn_new_fruit()
    spawn_monsters()
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

def combat():
    monsters[0].target = True

def monster_move():
    global monsters_loc, monsters
    if monsters[0].target:
        monsters[0].place 
    
    

def crash(new_snake_head):
    global snake_geometry, snake_direction, rocks
    if (
        new_snake_head in snake_geometry
        or new_snake_head in rocks
        or new_snake_head in monsters_loc
        or (
        new_snake_head[0] < 0
        or new_snake_head[0] > 29
        or new_snake_head[1] < 0
        or new_snake_head[1] > 29
        )
    ):
        return True
    return False


def snake_move():
    global snake_geometry, snake_direction, rocks
    snake_head = snake_geometry[-1]
    new_snake_head = [
        snake_head[0] + snake_direction[0],
        snake_head[1] + snake_direction[1],
    ]
    if p:
        return None
    if new_snake_head in monsters_loc:
        combat()
    if crash(new_snake_head):
        snake_geometry = snake_geometry[1:-1] + [snake_head]
    elif new_snake_head == fruit:
        snake_geometry = snake_geometry + [new_snake_head]
        spawn_everything()
    else:
        snake_geometry = snake_geometry[1:] + [new_snake_head]



def update():
    global maze_set, snake_geometry
    events.handle()
    monster_move()
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
    display(DARK_GREEN, snake_body)
    display(LIGHT_GREEN, [snake_head])
    display(BLACK, rocks)
    display(PINK, [fruit])


events.register(pyxel.KEY_Q, pyxel.quit)
events.register(pyxel.KEY_UP, move_up)
events.register(pyxel.KEY_DOWN, move_down)
events.register(pyxel.KEY_LEFT, move_left)
events.register(pyxel.KEY_RIGHT, move_right)
events.register(pyxel.KEY_P, pause)


pyxel.run(update, draw)