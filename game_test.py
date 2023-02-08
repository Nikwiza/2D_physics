from collision import *
from physics import *
import pygame
import numpy as np
import random
from objects import *
from pygame.locals import *

ch_height = 40
ch_width = 24
score = 0

class Player(object):
    def __init__(self):
        # self.rect = Rectangle(screen_width/2,screen_height-41,50,0.02,35,20)
        self.rect = Rectangle(screen_width/2-50,screen_height-50,50,0.02,ch_height,ch_width)

class Surface(object):
    def __init__(self, x, y, height, width):
        self.rect = Rectangle(x, y, 0, 0, height, width)

class Projectile(object):
    def __init__(self,x,y):
        # self.circle = Circle(x, y, 20, 0.1, 5) 
        self.circle = Rectangle(x, y, 0.1, 0.1, 15, 7)
        self.circle.angular_speed = 15

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
bg_image = pygame.image.load("img/index.png")
ch_image = pygame.image.load("img/char.jpg").convert_alpha()
pygame.transform.scale(ch_image, (ch_width, ch_height))
pygame.transform.scale(bg_image, (screen_width, screen_height))

surfaces.append(Surface(0, screen_height-16, 16, screen_width)) #bottom surface
surfaces.append(Surface(0, 0, screen_height-16, 16)) #left wall
surfaces.append(Surface(screen_width-16, 0, screen_height-16, 16)) #right wall
surfaces.append(Surface(0, 0, 16, screen_width)) #top surface

shotLoop = 0
running = True
key = ""
pause = False

Clock = pygame.time.Clock()

def drawGameWindow():
    screen.fill((0,0,0))
    screen.blit(bg_image, (0,0))
    player.rect.draw(screen, ch_image)
    
    #Score
    font = pygame.font.SysFont(None, 30)
    scr = font.render(str(score), True, "white")
    screen.blit(scr, (15,15))

    for bullet in bullets:
        bullet.circle.draw(screen, "gray")
    
    for surface in surfaces:
        surface.rect.draw(screen, "black")

    enemies.circle.draw(screen, "black")
    pygame.display.update()

while running:
    if pause:
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
            if (key[pygame.K_RETURN]):  # Enter key
                pause = False
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
            # cond1,_,_ = IntersectCircles(bullet.circle.position(), bullet.circle.circumference, enemies.circle.position(),enemies.circle.circumference)
            cond1,_,_ = IntersectCirclePolygon(enemies.circle.position(), enemies.circle.circumference, bullet.circle.Vertices())
            # cond2,_,_ = IntersectCirclePolygon(bullet.circle.position(), bullet.circle.circumference, surfaces[3].rect.Vertices())
            cond2,_,_ = IntersectPolygons(bullet.circle.Vertices(), surfaces[3].rect.Vertices())
            #if the bullet didn't hit the wall or exited the screen let him travel
            if cond1 == True:
                score+=1
            if cond1 == False and cond2 == False:
                bullet.circle.vel[1] = -50
                update(bullet.circle)
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
    
    else:
        key = pygame.key.get_pressed()
        for e in pygame.event.get():
            if (key[pygame.K_RETURN]): # Enter key
                pause = True
        drawGameWindow()




