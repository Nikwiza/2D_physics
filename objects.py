import pygame
from euler_meth import eulerN
from numpy import pi

#################################
#     OBJECT TEMPLATES MADE     #
#    TO WORK WITH THE ENGINE    #
#           AND PYGAME          #
#################################


# Instances that are colidable

collidable = []

########  CIRCLE  #########

class Circle:
    def __init__(self, x, y, mass, friction, circumference):

        self.mass = mass
        self.friction = friction
        self.circumference = circumference
        self.x = x
        self.y = y
        self.vel = [0.,0.]
        self.force = [0.,0.]
        self.surface = circumference**2 * pi
        collidable.append(self)

    #Drawing function : win -> pygame window

    def draw(self, win):
        pygame.draw.circle(win,(0,0,255), (self.x, self.y), self.circumference)

    

########  RECTANGLE  #########

class Rectangle:
    def __init__(self, x, y, mass, friction, height, width=-1):

        self.mass = mass
        self.friction = friction
        self.x = x
        self.y = y
        self.height = height
        self.force = [0.,0.]
        self.vel = [0.,0.]
        self.surface = height*width

        if width == -1:
            width = height
        
        self.width = width
        collidable.append(self)

    def draw(self, win):
        pygame.draw.rect(win,(0,0,255), (self.x, self.y, self.width, self.height))




