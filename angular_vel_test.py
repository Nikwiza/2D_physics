import pygame
import math
from euler_meth import eulerN
import numpy as np

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen = pygame.display.set_mode((400, 300))

#Some testing paramaters
surrounding_denc = 1 # Should not be 0, applied to all objects

ani_speed = 2.5 # Adjust the speed of the movement by adjusting the time difference 
fps = 60
dt = 1/fps # What distance is approximated 
t1 = 0 # Starting moment for approximation
t2 = t1+dt*ani_speed




# Define the rectangle class
class Rectangle:
    def __init__(self, x, y, width, height, angular_speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angular_speed = angular_speed
        self.torque = 0
        self.inertia = 1
        self.angle = 5
        self.color = "red"

    def update(self, dt):

        ddpA = lambda t, a, av : self.torque/self.inertia
        pnA = eulerN(t1, t2, t2-t1, np.array([self.angle, self.angular_speed]), ddpA)
        self.angle = pnA[0, -1]
        self. angular_speed = pnA[1,-1]
        

    def draw(self, screen):
        
        img = pygame.Surface((self.height, self.width))
        img.fill(self.color)
        img.set_colorkey("black") #test
        img = pygame.transform.rotate(img, self.angle)
        rect = img.get_rect()
        rect.center = (self.x//2, self.y//2)
        screen.blit(img, rect)

# Create the rectangle objects
rectangle1 = Rectangle(100, 150, 50, 50, 0)
rectangle1.torque = 1
rectangle1.inertia = 100
# rectangle2 = Rectangle(200, 150, 50, 50, 5)
rectangle3 = Rectangle(300, 150, 50, 50, 5)

# Set the clock for the simulation
clock = pygame.time.Clock()

# Set the running flag
running = True

# Start the simulation loop
while running:
    dt = 1/60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((100,100,100))

    # Update and draw the rectangles
    rectangle1.update(dt)
    rectangle1.draw(screen)
    # rectangle2.update(dt)
    # rectangle2.draw(screen)
    rectangle3.update(dt)
    rectangle3.draw(screen)

    pygame.display.update()

# Quit Pygame
pygame.quit()