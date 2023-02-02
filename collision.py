from pygame.locals import *
from pygame import Vector2
from objects import *
from math_util import *

pygame.init()

screen = pygame.display.set_mode((500,500))

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
        axis = Vector2(-edge.y, edge.x)
        axis = normalize(axis)
        #print(axis)

        [minA, maxA] = ProjectVertices(verticesA, axis)
        [minB, maxB] = ProjectVertices(verticesB, axis)

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
    min = Vector2.dot(vertices[0], axis)
    max = Vector2.dot(vertices[0], axis) 

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
    minDistance = distance(vertices[0], circleCenter)

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


sqr1 = Rectangle(250,150,1000,0.2,50)
sqr2 = Rectangle(120,150,1000,0.2,50)


running = True
key = ""
circle = Circle(150, 100, 1, 1, 20)
circle1 = Circle(200, 100, 1, 1, 20)
Clock = pygame.time.Clock()

while running:
    screen.fill((255,255,255))

    sqr1.draw(screen)
    #sqr2.draw(screen)

    circle.draw(screen)
    #circle1.draw(screen)

    

    vertices1 = sqr1.Vertices()
    #vertices2 = sqr2.Vertices()


    # IntersectPolygons(vertices1, vertices2)
    # # intersect of two polygons
    # if IntersectPolygons(vertices1, vertices2):
    #    sqr2.changeColor(col=(0,0,0))
    # else:
    #    sqr2.changeColor(col=(0,0,255))

    # Collision of two circles
    # cond, normal, depth = IntersectCircles(circle.position(), circle.circumference, circle1.position(), circle1.circumference)
    # if cond:
    #     circle.Move(-normal * depth / 2)
    #     circle1.Move(normal * depth / 2)

    #Collision of a circle and polygon
    cond, normal, depth = IntersectCirclePolygon(circle.position(), circle.circumference, vertices1)
    if(cond):
        sqr1.changeColor(col=(0,0,0))
    else:
        sqr1.changeColor(col=(0,0,255))

    if key == "s":
        circle.y += 1
    elif key == "w":
        circle.y -= 1
    if key == "d":
        circle.x += 1
    if key == "a":
        circle.x -= 1


    # if key == "s":
    #     sqr1.y += 1
    # elif key == "w":
    #     sqr1.y -= 1
    # if key == "d":
    #     sqr1.x += 1
    # if key == "a":
    #     sqr1.x -= 1

    pygame.display.update()
    Clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            running = False
        if e.type == MOUSEBUTTONDOWN:
            print(e.pos)
        if e.type == KEYDOWN:
            key = e.unicode
        if e.type == KEYUP:
            key = ""







    


    