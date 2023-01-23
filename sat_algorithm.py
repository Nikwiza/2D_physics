from pygame.locals import *
from pygame import Vector2
from objects import *

pygame.init()

screen = pygame.display.set_mode((500,500))

def IntersectPolygons(verticesA, verticesB):
    for i in range(len(verticesA)):
        v1 = verticesA[i] 
        v2 = verticesA[(i+1)%len(verticesA)]
        #edge of the polygon
        edge = v2 - v1
        #axis that we will project our vertices on
        axis = Vector2(-edge.y, edge.x)

        [minA, maxA] = ProjectVertices(verticesA, axis)
        [minB, maxB] = ProjectVertices(verticesB, axis)

        if(minA >= maxB or minB >= maxA):
            return False
    
    for i in range(len(verticesB)):
        v1 = verticesB[i]
        v2 = verticesB[(i+1)%len(verticesB)]
        #edge of the polygon
        edge = v2 - v1
        #axis that we will project our vertices on
        axis = Vector2(-edge.y, edge.x)

        [minA, maxA] = ProjectVertices(verticesA, axis)
        [minB, maxB] = ProjectVertices(verticesB, axis)

        if(minA >= maxB or minB >= maxA):
            return False
    
    return True
        

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

def RectanglesOverlap(rect1, rect2):
    # Check for overlap in the x dimension
    if rect1.x > rect2.x + rect2.width or rect2.x > rect1.x + rect1.width:
        return False
    # Check for overlap in the y dimension
    if rect1.y > rect2.y + rect2.height or rect2.y > rect1.y + rect1.height:
        return False
    # If we've made it this far, the rectangles are overlapping
    return True

def CircleRect(circle, rect):
    testX = circle.x
    testY = circle.y

    if(circle.x < rect.x):
        testX = rect.x #left edge
    elif(circle.x > (rect.x + rect.width)):
        testX = rect.x + rect.width #right edge
    
    if(circle.y < rect.y):
        testY = rect.y #top edge
    elif(circle.y > rect.y + rect.height):
        testY = rect.y + rect.height #bottom edge
    
    distX = circle.x - testX
    distY = circle.y - testY
    distance = math.sqrt((distX**2) + (distY**2))

    if(distance <= circle.circumference):
        return True
    
    return False
    
sqr1 = Rectangle(250,150,1000,0.2,50)
sqr2 = Rectangle(120,150,1000,0.2,50)


running = True
key = ""
circle = Circle(150, 100, 1, 1, 20)
Clock = pygame.time.Clock()

while running:
    screen.fill((0,0,0))

    sqr1.draw(screen)
    sqr2.draw(screen)

    vertices1 = sqr1.Vertices()
    vertices2 = sqr2.Vertices()

    if IntersectPolygons(vertices1, vertices2) and RectanglesOverlap(sqr1, sqr2):
        sqr2.changeColor(col=(0,0,0))
    else:
        sqr2.changeColor(col=(0,0,255))

    if key == "s":
        sqr1.y += 1
    elif key == "w":
        sqr1.y -= 1
    if key == "d":
        sqr1.x += 1
    if key == "a":
        sqr1.x -= 1

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







    


    