from pygame.locals import *
from pygame import Vector2
from objects import *

def IntersectPolygons(verticesA, verticesB, width, height):
    for i in range(len(verticesA)):
        v1 = verticesA[i] 
        v2 = verticesA[(i+1)%len(verticesA)]
        #edge of the polygon
        edge = v2 - v1
        #axis that we will project our vertices on
        axis = Vector2(-edge.y, edge.x)

        [minA, maxA] = ProjectVertices(verticesA, axis, width[0], height[0])
        [minB, maxB] = ProjectVertices(verticesB, axis, width[1], height[1])

        if(minA >= maxB or minB >= maxA):
            return False
    
    for i in range(len(verticesB)):
        v1 = verticesB[i]
        v2 = verticesB[(i+1)%len(verticesB)]
        #edge of the polygon
        edge = v2 - v1
        #axis that we will project our vertices on
        axis = Vector2(-edge.y, edge.x)

        [minA, maxA] = ProjectVertices(verticesA, axis, width[0], height[0])
        [minB, maxB] = ProjectVertices(verticesB, axis, width[1], height[1])

        if(minA >= maxB or minB >= maxA):
            return False
    
    return True
        

def ProjectVertices(vertices, axis, width, height):
    min = Vector2.dot(vertices[0], axis) + width
    max = Vector2.dot(vertices[0], axis) + height

    for v in vertices:
        #projection of a vertice onto an axis
        proj = Vector2.dot(v, axis) + width + height

        if proj < min:
            min = proj
        
        if proj > max:
            max = proj
    
    return [min, max]








    


    