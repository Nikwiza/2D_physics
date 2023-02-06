import pygame
from euler_meth import eulerN
from pygame import Vector2
from numpy import pi
import math
from pygame.locals import *

#################################
#     OBJECT TEMPLATES MADE     #
#    TO WORK WITH THE ENGINE    #
#           AND PYGAME          #
#################################


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
        self.grounded = False

    #Drawing function : win -> pygame window

    def Move(self, amount):
        self.x += amount.x
        self.y += amount.y

    def position(self):
        return Vector2(self.x, self.y)

    def draw(self, win, col):
        pygame.draw.circle(win, col, (self.x, self.y), self.circumference)
    

    

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
        self.grounded = False

        if width == -1:
            self.width = height
        else:
            self.width = width

        self.surface = self.height*self.width

        self.centerx = self.x + self.width//2
        self.centery = self.y + self.height//2
        self.rotation_angle = 0


    def GetCorner(self, tempX, tempY):
        #translate
        x = tempX + self.centerx
        y = tempY + self.centery
        angle = math.radians(self.rotation_angle)
        #apply rotation
        rotatedX = x*math.cos(angle) - y*math.sin(angle)
        rotatedY = x*math.sin(angle) + y*math.cos(angle)
        
        return Vector2(rotatedX,rotatedY)
    
    def Vertices(self):
        v1 = self.GetCorner(self.x - self.centerx, self.y - self.centery) #top, left
        v2 = self.GetCorner(self.x + self.width - self.centerx, self.y - self.centery) #top, right
        v3 = self.GetCorner(self.x - self.centerx, self.y + self.height - self.centery) #bottom, left
        v4 = self.GetCorner(self.x + self.width - self.centerx, self.y + self.height - self.centery) #bottom, right
        
        return [v1, v2, v3, v4]
        
    def draw(self, win, col):
            pygame.draw.rect(win, col, (self.x, self.y, self.width, self.height))
    
    def Move(self, amount):
            self.x += amount.x
            self.y += amount.y
    
    




