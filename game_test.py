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
        self.rect = Rectangle(screen_width/2-50,screen_height-50,50,0.02,ch_height,ch_width)

class Surface(object):
    def __init__(self, x, y, height, width):
        self.rect = Rectangle(x, y, 0, 0, height, width)

class Projectile(object):
    def __init__(self,x,y):
        self.rect = Rectangle(x, y, 0.1, 0.1, 24, 10)
        self.rect.angular_speed = 15

    def draw(self,win):
        self.rect(win)

class Enemy(object):
    def __init__(self, x, y, circumference):
        self.circle = Circle(x, y, 100, 0.01, circumference)
        self.circle.cor = 1.3
        self.health = 10

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
    
    def draw(self, screen):
        enemy.circle.draw(screen, enemy_image)
        #health bar
        hb_pos_x = enemy.circle.x-enemy.circle.circumference
        hb_pos_y = enemy.circle.y-enemy.circle.circumference-10
        diameter = enemy.circle.circumference*2
        pygame.draw.rect(screen, (255, 0, 0), (hb_pos_x, hb_pos_y, diameter, 10))
        pygame.draw.rect(screen, (0, 128, 0), (hb_pos_x, hb_pos_y, diameter - ((diameter/10) * (10 - self.health)), 10))
    

pygame.init()

screen_height = 400
screen_width = 700

screen = pygame.display.set_mode((screen_width, screen_height))


enemy = Enemy(screen_width//2, 46, 30)
player = Player()
bullets = []
#floor and walls
surfaces = []
bg_image = pygame.image.load("img/index.png")
ch_image = pygame.image.load("img/char.jpg").convert_alpha()
enemy_image = pygame.image.load("img/Enemy.png").convert_alpha()
sword_image = pygame.image.load("img/Sword.png").convert_alpha()
pygame.transform.scale(ch_image, (ch_width, ch_height))
pygame.transform.scale(bg_image, (screen_width, screen_height))

surfaces.append(Surface(0, screen_height-16, 16, screen_width)) #bottom surface
surfaces.append(Surface(0, 0, screen_height-16, 8)) #left wall
surfaces.append(Surface(screen_width-16, 0, screen_height-16, 8)) #right wall
surfaces.append(Surface(0, 0, 1, screen_width)) #top surface

shotLoop = 0
running = True
key = ""
pause = False

Clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

def drawText(text, font, text_col, x, y):
    scr = font.render(text, True, text_col)
    screen.blit(scr, (x,y))

def drawGameWindow():
    screen.fill((0,0,0))
    screen.blit(bg_image, (0,0))
    player.rect.draw(screen, ch_image)
    
    #Score
    drawText(str(score), font, "white", 15, 15)

    #Pause screen
    if(pause == False):
        drawText("CLICK ENTER TO UNPAUSE", font, "white", screen_width/2-132, screen_height/2)

    for bullet in bullets:
        bullet.rect.draw(screen, sword_image )
    
    for surface in surfaces:
        surface.rect.draw(screen, "black")

    enemy.draw(screen)

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
                    
        enemy.update()

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
            #If the bullet hits the enemy
            cond1 = IntersectCirclePolygon(enemy.circle.position(), enemy.circle.circumference, bullet.rect.Vertices())[0]
            #If the bullet exits the screen
            cond2 = IntersectPolygons(surfaces[3].rect.Vertices(), bullet.rect.Vertices())[0]
            
            if cond1 == True:
                score+=1
                if(enemy.health == 0):
                    running = False
                enemy.health -= 1
            #If the bullet didn't hit the enemy or exited the screen let him travel    
            if cond1 == False and cond2 == False:
                bullet.rect.vel[1] = -50
                update(bullet.rect)
            else:
                bullets.remove(bullet)

        for surface in surfaces:
            cond, normal, depth = IntersectPolygons(surface.rect.Vertices(), player.rect.Vertices())
            if(cond):
                player.rect.Move(normal * depth)

            cond1, normal1, depth1 = IntersectCirclePolygon(enemy.circle.position(), enemy.circle.circumference, surface.rect.Vertices())
            if cond1:
                enemy.circle.Move(normal1 * depth1)
                enemy.bounce(normal1, 0.9)  
            
        cond, normal, depth = IntersectCirclePolygon(enemy.circle.position(), enemy.circle.circumference, player.rect.Vertices())
        if(cond):
            running = False

        update(enemy.circle)
        update(player.rect)

        drawGameWindow()
        
    else:
        key = pygame.key.get_pressed()
        for e in pygame.event.get():
            if (key[pygame.K_RETURN]): # Enter key
                pause = True
        drawGameWindow()


