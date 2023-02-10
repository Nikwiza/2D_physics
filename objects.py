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
        self.grounded = False
        self.cor = 1 #coefficient of restitution

        # Angular movement
        self.rotation_angle = 0
        self.angular_speed = 0
        self.torque = 0
        self.inertia_mom = 1


        collidable.append(self)

    #Drawing function : win -> pygame window

    def Move(self, amount):
        self.x += amount.x
        self.y += amount.y

    def position(self):
        return Vector2(self.x, self.y)

    def draw(self, win, col):
        #pygame.draw.circle(win, "dark green", (self.x, self.y), self.circumference)
        if(type(col) == pygame.Surface):
            img = col
            img = pygame.transform.rotate(img, self.rotation_angle)
            rect = img.get_rect()
            rect.center = (self.x, self.y)
            win.blit(img, rect)
        else:
            pygame.draw.circle(win, "dark green", (self.x, self.y), self.circumference)
        
    

    

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
        self.grounded = False

        if width == -1:
            self.width = height
        else:
            self.width = width

        # Angular movement
        self.rotation_angle = 0
        self.angular_speed = 0
        self.torque = 0
        self.inertia_mom = 1

        self.surface = self.height*self.width
        self.centerx = self.x + self.width//2
        self.centery = self.y + self.height//2

        collidable.append(self)


    def GetCorner(self, tempX, tempY):
        angle = math.radians(self.rotation_angle)
        rotatedX = tempX*math.cos(angle) - tempY*math.sin(angle)
        rotatedY = tempX*math.sin(angle) + tempY*math.cos(angle)  

        x = rotatedX + self.centerx
        y = rotatedY + self.centery        

        return Vector2(x,y)
    
    def Vertices(self):
        v1 = self.GetCorner(self.x - self.centerx, self.y - self.centery) #top, left
        v2 = self.GetCorner(self.x + self.width - self.centerx, self.y - self.centery) #top, right
        v3 = self.GetCorner(self.x - self.centerx, self.y + self.height - self.centery) #bottom, left
        v4 = self.GetCorner(self.x + self.width - self.centerx, self.y + self.height - self.centery) #bottom, right
        
        return [v1, v2, v3, v4]
        
    def draw(self, win, col):
        if(type(col) == pygame.Surface):
            img = col
        else:
            img = pygame.Surface((self.width, self.height))
            img.fill(col)
            img.set_colorkey("black")
        img = pygame.transform.rotate(img, self.rotation_angle)
        rect = img.get_rect()
        rect.center = (self.x+(self.width//2), self.y+ (self.height//2))
        win.blit(img, rect)
        
    
    def Move(self, amount):
            self.x += amount.x
            self.y += amount.y
    
    




