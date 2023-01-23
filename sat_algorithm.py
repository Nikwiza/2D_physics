import pygame
from pygame.locals import *
from pygame import Vector2
import math
from objects import *
import sat_test

pygame.init()

screen = pygame.display.set_mode((500,500))

#Algorithm to find if 2 lines intersect
def LineIntersect(line1, line2):
    #line1 = ((x1, y1), (x2, y2))
    x1 = line1[0].x
    y1 = line1[0].y
    x2 = line1[1].x
    y2 = line1[1].y
    #line2 = ((x3, y3), (x4, y4))
    x3 = line2[0].x
    y3 = line2[0].y
    x4 = line2[1].x
    y4 = line2[1].y

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    #can't divide by 0
    if den == 0:
        return
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4))/den
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2))/den

    if t > 0 and t < 1 and u > 0 and u < 1:
        point = Vector2()
        point.x = x1 + t * (x2 - x1)
        point.y = y1 + t * (y2 - y1)
        return point
    return

def DrawLineInBetween(sqr1, sqr2):
    #print(sqr1.centerx)
    #print(sqr1.centery)
    #draw a line between the 2 squares, get gradient
    #to avoid divide by zero
    if abs(sqr1.x - sqr2.x) == 0:
        gradient = "infinity"
    else:
        #rise over run
        #left - right = run
        left = sqr1 if sqr1.x < sqr2.x else sqr2
        right = sqr1 if left == sqr2 else sqr2
        gradient = ((left.y - right.y)/abs(sqr1.x - sqr2.x))

    #get the middle point between the centers of the squares
    middle = (max(sqr1.x + sqr1.width//2, sqr2.x + sqr2.width//2) - abs(sqr1.x - sqr2.x)//2,
              max(sqr1.y + sqr1.width//2, sqr2.y + sqr2.width//2) - abs(sqr1.y - sqr2.y)//2)
    #to avoid divide by 0
    if gradient == 0:
        point1 = Vector2(middle[0], middle[1] + 100)
        point2 = Vector2(middle[0], middle[1] - 100)
    elif gradient == "infinity":
        point1 = Vector2(middle[0] - 100, middle[1])
        point2 = Vector2(middle[0] + 100, middle[1])        
    else:
        #get normal of line
        gradient = -1/gradient
        #print("normal:",gradient)

        point1 = Vector2(middle[0] + 100, middle[1] + int(-100 * gradient))
        point2 = Vector2(middle[0] - 100, middle[1] + int(100 * gradient))
        #print(point1)
        #print(point2)
        #print(middle)

    pygame.draw.line(screen,(0,255,0),point1,point2,1)

    line = (point1, point2)
    return line


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


#Test example

sqr1 = Rectangle(250,150,1000,0.2,50)
sqr2 = Rectangle(190,150,1000,0.2,50)
circle = Circle(150, 100, 1, 1, 20)
Clock = pygame.time.Clock()

running = True
key = ""

while running:
    screen.fill((0,0,0))

    sqr1.draw(screen)
    sqr2.draw(screen)
    #circle.draw(screen)
    line = DrawLineInBetween(sqr1, sqr2)
    pt1, pt2 = 0, 0
    
    for sqr_line in sqr1.Lines():
       pt1 = LineIntersect(line,sqr_line)
       if pt1 and pt2:
            pygame.draw.circle(screen,(0,255,255),(int(pt1.x),int(pt1.y)),5)
    
    for sqr_line in sqr2.Lines():
       pt2 = LineIntersect(line,sqr_line)
       if pt2 and pt1:
            pygame.draw.circle(screen,(0,255,255),(int(pt2.x),int(pt2.y)),5)
    
        
        
    
    #VerticesA = [sqr1.v1, sqr1.v2, sqr1.v3, sqr1.v4]
    #VerticesB = [sqr2.v1, sqr2.v2, sqr2.v3, sqr2.v4]
    #if(sat_test.IntersectPolygons(VerticesA, VerticesB, [sqr1.width, sqr2.width], [sqr1.height, sqr2.height])):
     #  sqr2.changeColor(screen)
    #else:
     #  sqr2.draw(screen)
   # if(CircleRect(circle, sqr2)):
        #sqr2.changeColor(screen)
      #  sqr2.x = 0
     #   sqr2.y = 0
    #else:
     #   sqr2.draw(screen)

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

    


    