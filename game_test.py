import collision
import physics
import pygame
from objects import *

pygame.init()
win = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Physics test")

##############  TEST RUN  ###################

x = 200 
y = 200

width = 20
height = 20

test = Rectangle(x, y, 1000, 0.2, width, height)
platform = Rectangle(x, y, 0, 0, 20, 800)
#test_c = Circle(x+30, y+30, 100, 0.2, 30)

movable = []
movable.append(test)

vel = 10
run = True

while run:
    pygame.time.delay(10)
    
    platform.draw(win)

    cond, normal, depth = collision.IntersectPolygons(test.Vertices(), platform.Vertices())

    if(cond):
        test.vel = [0, 0]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and test.x>0:
        test.vel[0]-=vel
    
    if keys[pygame.K_RIGHT] and test.x<800-width:
        test.vel[0]+=vel
    
    if keys[pygame.K_DOWN] and test.y<800-height:
        test.vel[1]+=vel

    if keys[pygame.K_UP] and test.y>0:
        test.vel[1]-=vel

    if test.y > 800:
        test.grounded = True


    win.fill((0,0,0))
    physics.update(win, movable)
    pygame.display.update()

pygame.quit()

