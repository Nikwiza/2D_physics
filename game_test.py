from collision import *
from physics import *
import pygame
import numpy as np
import random
from objects import *

class Player(object):
    def __init__(self):
        self.rect = Rectangle(screen_width/2,screen_height-41,50,0.02,35,20)

class Surface(object):
    def __init__(self, x, y, height, width):
        self.rect = Rectangle(x, y, 0, 0, height, width)

class Projectile(object):
    def __init__(self,x,y):
        self.circle = Circle(x, y, 20, 0.1, 5)

    def draw(self,win):
        self.circle(win)

class Enemy(object):
    def __init__(self, x, y, circumference):
        self.circle = Circle(x, y, 100, 0.01, circumference)
        #screen_width//2, 46, 50, 0.01, 20
        self.circle.cor = 1.3

    def update(self):
        self.circle.x += self.circle.vel[0]
        self.circle.y += self.circle.vel[1]
    
    def bounce(self, normal, damping_factor):
        reflected_velocity = self.circle.vel - (1 + self.circle.cor) * np.dot(self.circle.vel, normal) * normal

        #apply damping factor
        reflected_velocity *= damping_factor

        #generate a random deviation
        deviation = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        deviation = deviation / np.linalg.norm(deviation)

        #add the random deviation to the reflected velocity
        new_velocity = reflected_velocity + deviation

        self.circle.vel = new_velocity
        #update position based on new velocity
        self.circle.x += self.circle.vel[0]
        self.circle.y += self.circle.vel[1]

pygame.init()

screen_height = 400
screen_width = 700

screen = pygame.display.set_mode((screen_width, screen_height))


enemies = Enemy(screen_width//2, 46, 30)
player = Player()
bullets = []
#floor and walls
surfaces = []

surfaces.append(Surface(0, screen_height-16, 16, screen_width)) #bottom surface
surfaces.append(Surface(0, 0, screen_height-16, 16)) #left wall
surfaces.append(Surface(screen_width-16, 0, screen_height-16, 16)) #right wall
surfaces.append(Surface(0, 0, 16, screen_width)) #top surface

shotLoop = 0
running = True
key = ""

Clock = pygame.time.Clock()

def drawGameWindow():
    screen.fill((255,255,255))
    player.rect.draw(screen, "green")

    for bullet in bullets:
        bullet.circle.draw(screen, "red")
    
    for surface in surfaces:
        surface.rect.draw(screen, "black")

    enemies.circle.draw(screen, "black")
    pygame.display.update()

while running:
    Clock.tick(60)

    if(shotLoop > 0):
        shotLoop += 1
    if(shotLoop > 3):
        shotLoop = 0
    
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.rect.x += -2
    if key[pygame.K_RIGHT]:
        player.rect.x += 2
            
    enemies.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and shotLoop == 0:
                if(len(bullets) < 5):
                    bullets.append(Projectile(round(player.rect.x + player.rect.width//2), round(player.rect.y + player.rect.height//2)))

                shotLoop = 1

    for bullet in bullets:
        cond1,_,_ = IntersectCircles(bullet.circle.position(), bullet.circle.circumference, enemies.circle.position(),enemies.circle.circumference)
        cond2,_,_ = IntersectCirclePolygon(bullet.circle.position(), bullet.circle.circumference, surfaces[3].rect.Vertices())
        #if the bullet didn't hit the wall or exited the screen let him travel
        if cond1 == False and cond2 == False:
            bullet.circle.y -= 2
        else: 
            bullets.remove(bullet)

    for surface in surfaces:
        cond, normal, depth = IntersectPolygons(surface.rect.Vertices(), player.rect.Vertices())
        if(cond):
            player.rect.Move(normal * depth)

        cond1, normal1, depth1 = IntersectCirclePolygon(enemies.circle.position(), enemies.circle.circumference, surface.rect.Vertices())

        if cond1:
            enemies.circle.Move(normal1 * depth1)
            enemies.bounce(normal1, 0.9)  
    
    cond, normal, depth = IntersectCirclePolygon(enemies.circle.position(), enemies.circle.circumference, player.rect.Vertices())
    if(cond):
        running = False

    update(enemies.circle)
    update(player.rect)

    drawGameWindow()
    

