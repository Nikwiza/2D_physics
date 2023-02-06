from euler_meth import eulerN
import numpy as np
import pygame

# g -> Gravitational constant
g = 9.81
surrounding_denc = 1 # Should not be 0, applied to all objects

ani_speed = 2.5 # Adjust the speed of the movement by adjusting the time difference 
fps = 60
dt = 1/fps # What distance is approximated 
t1 = 0 # Starting moment for approximation
t2 = t1+dt*ani_speed

# Normalizeing a vector

def normalize(vec):
    magnitude = np.linalg.norm(vec, 2)
    if magnitude == np.inf or magnitude <= 0:
        ret = [1,0]

    else:
        ret = vec/magnitude

    return ret
        
# Use a force on an object

def force(o, force):
    force = normalize(force)
    o.force += force
    return

def update(win, o): 
        # F are all the forces acting on the body
        
        Fa = np.array(o.force)
        gr = o.mass*g
        Fg = np.array([0,gr])

        # Fd represents the drag, it takes into account velocity, friction, surrounding denc and the surface of the object
        Fd = -(np.array([abs(o.vel[0]),abs(o.vel[1])])*o.friction*o.surface*surrounding_denc)*normalize(o.vel)
        F = Fg+Fa+Fd



        # Fg -> gravity
        # Fa -> Applied forces
        # Fd -> Drag
        ddpX = lambda t, p, v: F[0]/o.mass
        ddpY = lambda t, p, v: F[1]/o.mass
        
        pnX = eulerN(t1, t2, t2 - t1, np.array([o.x, o.vel[0]]), ddpX)  
        pnY = eulerN(t1, t2, t2 - t1, np.array([o.y, o.vel[1]]), ddpY) 
        
        o.x = pnX[0, -1]
        o.y = pnY[0, -1]

        # If the object is grounded, the y position is returned to 0
        if o.grounded:
            _, pos = pygame.display.get_surface().get_size()
            o.y = pos-o.height

        o.vel = [pnX[1, -1], pnY[1, -1]]

