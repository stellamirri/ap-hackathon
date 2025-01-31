import numpy as np
import random as rd
import pyxel

'''
map 60*110
5 pieces reliées
'''

startpos1 = []
for i in range(5):
    for j in range(10):
        startpos1.append((1+i, 1+j))
dims1 = range(7,16)

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
    for i in range(doornumber):
        doors.add(rd.choice(walls))
    walls = walls-inside-doors

    return walls, inside, doors

walls1, inside1 = generate_room(startpos1, dims1, 2)
