import pygame
from pygame.locals import *
from pygame import Vector2
import math
from objects import *

def IntersectPolygons(verticesA, verticesB):
    for i in range(0, len(verticesA)):
        va = verticesA[i] 
        vb = verticesA[(i+1)%len(verticesA)]
        #edge of the polygon
        edge = vb - va
        #axis that we will project our vertices on
        axis = Vector2(-edge.y, edge.x)

        [minA, maxA] = ProjectVertices(verticesA, axis)
        [minB, maxB] = ProjectVertices(verticesB, axis)

        if(minA >= maxB or minB >= maxA):
            return False
    
    for i in range(0, len(verticesB)):
        va = verticesB[i]
        vb = verticesB[(i+1)%len(verticesB)]
        #edge of the polygon
        edge = vb - va
        #axis that we will project our vertices on
        axis = Vector2(-edge.y, edge.x)

        [minA, maxA] = ProjectVertices(verticesA, axis)
        [minB, maxB] = ProjectVertices(verticesB, axis)

        if(minA >= maxB or minB >= maxA):
            return False
    
    return True
        

def ProjectVertices(vertices, axis):
    min = math.inf
    max = -math.inf

    for v in vertices:
        #projection of a vertice onto an axis
        proj = Vector2.dot(v, axis)

        if proj < min:
            min = proj
        
        if proj > max:
            max = proj
    
    return [min, max]








    


    