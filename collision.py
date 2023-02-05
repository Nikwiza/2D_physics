from pygame.locals import *
from pygame import Vector2
from objects import *
from math_util import *

pygame.init()

screen_height = 500
screen_width = 500

screen = pygame.display.set_mode((screen_height,screen_width))

def IntersectPolygons(verticesA, verticesB):
    depth = math.inf
    normal = Vector2(0,0)
    for i in range(len(verticesA)):
        v1 = verticesA[i] 
        v2 = verticesA[(i+1)%len(verticesA)]
        #edge of the polygon
        edge = v2 - v1
        #axis that we will project our vertices on
        axis = Vector2(-edge.y, edge.x)
        axis = normalize(axis)

        [minA, maxA] = ProjectVertices(verticesA, axis)
        [minB, maxB] = ProjectVertices(verticesB, axis)

        if(minA >= maxB or minB >= maxA):
            return False, 0, 0
        
        axisDepth = min(maxB - minA, maxA - minB)

        if(axisDepth < depth):
            depth = axisDepth
            normal = axis
    
    for i in range(len(verticesB)):
        v1 = verticesB[i]
        v2 = verticesB[(i+1)%len(verticesB)]
        #edge of the polygon
        edge = v2 - v1
        #axis that we will project our vertices on
        axis = Vector2(-edge.x, edge.y)
        axis = normalize(axis)

        [minA, maxA] = ProjectVertices(verticesA, axis)
        [minB, maxB] = ProjectVertices(verticesB, axis)

        # screen.fill("red", (Vector2(minA,axis.y), (3, 3)))
        # screen.fill("red", (Vector2(maxA,axis.y), (3, 3)))
        # screen.fill("green", (Vector2(minB,axis.y), (3, 3)))
        # screen.fill("green", (Vector2(maxB,axis.y), (3, 3)))
        if(minA >= maxB or minB >= maxA):
            return False, 0, 0

        axisDepth = min(maxB - minA, maxA - minB)

        if(axisDepth < depth):
            depth = axisDepth
            normal = axis

    centerA = findArithmeticMean(verticesA)
    centerB = findArithmeticMean(verticesB)

    direction = centerB - centerA

    if(Vector2.dot(direction, normal) < 0):
        normal = -normal

    return True, normal, depth
        
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

def IntersectCircles(centerA, radiusA, centerB, radiusB):
    dist = distance(centerA, centerB)
    radius = radiusA + radiusB

    if(dist >= radius):
        return False, 0, 0

    normal = normalize(centerB - centerA)
    depth = radius - dist

    return True, normal, depth

def IntersectCirclePolygon(circleCenter, circleRadius, vertices):
    depth = math.inf
    normal = Vector2(0,0)

    for i in range(len(vertices)):
        v1 = vertices[i] 
        v2 = vertices[(i+1)%len(vertices)]
        #edge of the polygon
        edge = v2 - v1
        #axis that we will project our vertices on
        axis = Vector2(-edge.y, edge.x)
        axis = normalize(axis)

        [minA, maxA] = ProjectVertices(vertices, axis)
        [minB, maxB] = ProjectCircle(circleCenter, circleRadius, axis)

        if(minA >= maxB or minB >= maxA):
            return False, 0, 0
        
        axisDepth = min(maxB - minA, maxA - minB)

        if(axisDepth < depth):
            depth = axisDepth
            normal = axis
    
    cpIndex = FindClosestPointOnPolygon(circleCenter, vertices)
    cp = vertices[cpIndex]

    axis = cp - circleCenter
    axis = normalize(axis)

    [minA, maxA] = ProjectVertices(vertices, axis)
    [minB, maxB] = ProjectCircle(circleCenter, circleRadius, axis)


    if(minA >= maxB or minB >= maxA):
            return False, 0, 0
    
    axisDepth = min(maxB - minA, maxA - minB)

    if(axisDepth < depth):
        depth = axisDepth
        normal = axis
    
    polygonCenter = findArithmeticMean(vertices) #find the center of polygon
    direction = polygonCenter - circleCenter

    if(Vector2.dot(direction, normal) < 0):
        normal = -normal
    

    return True, normal, depth

def FindClosestPointOnPolygon(circleCenter, vertices):
    result = -1
    minDistance = math.inf

    for i in range(len(vertices)):
        v = vertices[i] 
        dist = distance(v, circleCenter)

        if(dist < minDistance):
            minDistance = dist
            result = i

    return result

def ProjectCircle(center, radius, axis):
    direction = normalize(axis)
    directionAndRadius = direction * radius

    p1 = center + directionAndRadius
    p2 = center - directionAndRadius

    min = Vector2.dot(p1, axis) #project first point onto an axis
    max = Vector2.dot(p2, axis) #project second point onto an axis

    if(min > max):
        #swap values
        min, max = max, min

    return min, max









    


    