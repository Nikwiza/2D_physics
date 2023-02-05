from collision import *
from physics import *
import pygame
from objects import *

class Player(object):
    def __init__(self):
        self.rect = Rectangle(40,40,50,0.2,16)

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = Rectangle(pos[0], pos[1], 0, 0, 16, 16)

pygame.init()

screen_height = 512
screen_width = 256

screen = pygame.display.set_mode((screen_height,screen_width))


walls = []
player = Player()

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

running = True
key = ""

Clock = pygame.time.Clock()

while running:
    pygame.display.update()
    Clock.tick(60)

    
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.rect.x += -2
    if key[pygame.K_RIGHT]:
        player.rect.x += 2
    if key[pygame.K_UP]:
        player.rect.y += -2
    if key[pygame.K_DOWN]:
        player.rect.y += 2

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    for wall in walls:
        cond, normal, depth = IntersectPolygons(wall.rect.Vertices(), player.rect.Vertices())
        if(cond):
            player.rect.Move(normal * depth / 2)

    screen.fill((255,255,255))
    player.rect.draw(screen)
    for wall in walls:
        wall.rect.changeColor((255,255,255))
        wall.rect.draw(screen)
    

