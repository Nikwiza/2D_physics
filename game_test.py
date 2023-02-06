from collision import *
from physics import *
import pygame
from objects import *

class Player(object):
    def __init__(self):
        self.rect = Rectangle(screen_height/2,screen_width-32,50,0.2,16)

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = Rectangle(pos[0], pos[1], 0, 0, 16, 16)

class Projectile(object):
    def __init__(self,x,y):
        self.circle = Circle(x, y, 20, 0.1, 5)

    def draw(self,win):
        self.circle(win)

class Enemy(object):
    def __init__(self):
        self.circle = Circle(screen_height/2, 0, 200, 0.1, 30)

pygame.init()

screen_height = 512
screen_width = 256

screen = pygame.display.set_mode((screen_height,screen_width))


walls = []
enemies = Enemy()
player = Player()
bullets = []

level = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "W                              W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]

x = y = 0

for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        x += 16
    y += 16
    x = 0

shotLoop = 0
running = True
key = ""

Clock = pygame.time.Clock()

def drawGameWindow():
    screen.fill((255,255,255))
    player.rect.draw(screen)
    for wall in walls:
        wall.rect.changeColor((255,255,255))
        wall.rect.draw(screen)

    for bullet in bullets:
        bullet.circle.draw(screen, "red")
            
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
        cond1, _, _ = IntersectCircles(bullet.circle.position(), bullet.circle.circumference, enemies.circle.position(),enemies.circle.circumference)
        for wall in walls:
            cond2, _, _ = IntersectCirclePolygon(bullet.circle.position(), bullet.circle.circumference, wall.rect.Vertices())

        if cond1 == False and cond2 == False:
            bullet.circle.y -= 2
        else:
            bullets.remove(bullet)

    for wall in walls:
        cond, normal, depth = IntersectPolygons(wall.rect.Vertices(), player.rect.Vertices())
        if(cond):
            player.rect.Move(normal * depth / 2)

    
    cond, normal, depth = IntersectCirclePolygon(enemies.circle.position(), enemies.circle.circumference, player.rect.Vertices())
    if(cond):
        running = False

    update(screen, enemies.circle)
    
    drawGameWindow()
    

