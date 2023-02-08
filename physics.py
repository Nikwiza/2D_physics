from euler_meth import eulerN
import numpy as np
import pygame
import objects

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

def update(o): 
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
        ddpA = lambda t, a, av : o.torque/o.inertia_mom
        
        pnX = eulerN(t1, t2, t2 - t1, np.array([o.x, o.vel[0]]), ddpX)  
        pnY = eulerN(t1, t2, t2 - t1, np.array([o.y, o.vel[1]]), ddpY) 


        # Updateing rotation
        pnA = eulerN(t1, t2, t2-t1, np.array([o.rotation_angle, o.angular_speed]), ddpA)
        o.rotation_angle = pnA[0, -1]
        o.angular_speed = pnA[1,-1]

        o.x = pnX[0, -1]
        o.y = pnY[0, -1]

        #Updateing the center lines

        if(type(o) == objects.Rectangle):
            o.centerx = o.x + o.width//2
            o.centery = o.y + o.height//2

        # If the object is grounded, the y position is returned to 0
        if o.grounded:
            _, pos = pygame.display.get_surface().get_size()
            o.y = pos-o.height

        o.vel = [pnX[1, -1], pnY[1, -1]]

def update_all(win):
     for o in objects.collidable:
        

        # F are all the forces acting on the body
        
        Fa = np.array(o.force)
        gr = o.mass*g
        Fg = np.array([0,gr])

        # Fd represents the drag, it takes into account velocity, friction, surrounding denc and the surface of the object
        Fd = -(np.array([abs(o.vel[0]),abs(o.vel[1])])*o.friction*o.surface*surrounding_denc)*normalize(o.vel)
        F = Fg+Fa+Fd

        # The equations for torque and moment of inertia need work


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
        print("Velocity_after")
        print(o.vel)
        o.draw(win, "yellow")

