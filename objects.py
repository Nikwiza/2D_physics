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

        if width == -1:
            self.width = height
        else:
            self.width = width

        self.surface = self.height*self.width

        self.centerx = self.x + self.width//2
        self.centery = self.y + self.height//2
        self.col = (255, 0, 0)
        self.rotation_angle = 0

        #vertices
        self.v1 = self.GetCorner(self.x - self.centerx, self.y - self.centery) #top, left
        self.v2 = self.GetCorner(self.x + self.width - self.centerx, self.y - self.centery) #top, right
        self.v3 = self.GetCorner(self.x - self.centerx, self.y + self.width - self.centery) #bottom, left
        self.v4 = self.GetCorner(self.x + self.width - self.centerx, self.y + self.width - self.centery) #bottom, right

        collidable.append(self)

    def GetCorner(self, tempX, tempY):
        #translate
        x = tempX + self.centerx
        y = tempY + self.centery
        angle = math.radians(self.rotation_angle)
        #apply rotation
        rotatedX = x*math.cos(angle) - y*math.sin(angle)
        rotatedY = x*math.sin(angle) + y*math.cos(angle)
       
        return Vector2(rotatedX,rotatedY)

    def Outline(self, win):
        for point1, point2 in self.Lines():
            pygame.draw.line(win,self.col,point1,point2,1)
    
    def Lines(self):
        lines = []
        top_left = self.GetCorner(self.x - self.centerx, self.y - self.centery)
        top_right = self.GetCorner(self.x + self.width - self.centerx, self.y - self.centery)
        bottom_left = self.GetCorner(self.x - self.centerx, self.y + self.width - self.centery)
        bottom_right = self.GetCorner(self.x + self.width - self.centerx, self.y + self.width - self.centery)

        lines.append((top_left, top_right))
        lines.append((top_left, bottom_left))
        lines.append((bottom_right, top_right))
        lines.append((bottom_right, bottom_left))
        return lines

    def draw(self, win, outline=False):
        if outline:
            self.Outline()
        else:
            pygame.draw.rect(win,(0,0,255), (self.x, self.y, self.width, self.height))
    
    def Move(self, x=None, y=None):
        if x:
            self.x += x
            self.centerx += x
        if y:
            self.y += y
            self.centery += y
    
    def changeColor(self, win):
        pygame.draw.rect(win,(255,0,0), (self.x, self.y, self.width, self.height))
    




