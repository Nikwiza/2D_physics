from euler_meth import eulerN
import objects
import numpy as np

# g -> Gravitational constant
g = 9.81
surrounding_denc = 0.3 # Should not be 0, applied to all objects
drag_c = 0.5 # Used to further finetune the drag

ani_speed = 2.5 # Adjust the speed of the movement by adjusting the time difference 
fps = 60
dt = 1/fps # What distance is approximated 
t1 = 0 # Starting moment for approximation
t2 = t1+dt*ani_speed

#Todo: noralize The force applied 

def update(win): 
    for o in objects.collidable:
        

        # F are all the forces acting on the body
        
        Fa = np.array(o.force)
        gr = o.mass*g
        Fg = np.array([0,gr])

        # Fd represents the drag, it takes into account velocity, friction, surrounding denc and the surface of the object
        #Fd = np.array(o.vel)*np.linalg.norm(o.vel, 2)*drag_c*surrounding_denc*o.friction * o.surface
        Fd = np.array([abs(o.vel[0]),abs(o.vel[1])])*o.friction
        F = Fg+Fa-Fd

        print(type(o), Fg, Fd)

        # Fg -> gravity
        # Fa -> Applied forces
        # Fd -> Drag
        ddpX = lambda t, p, v: F[0]/o.mass
        ddpY = lambda t, p, v: F[1]/o.mass
        
        pnX = eulerN(t1, t2, dt, np.array([o.x, o.vel[0]]), ddpX)  
        pnY = eulerN(t1, t2, t2 - t1, np.array([o.y, o.vel[1]]), ddpY) 
        o.x = pnX[0, -1]
        o.y = pnY[0, -1]
        o.vel = [pnX[1, -1], pnY[1, -1]]

        o.draw(win)

