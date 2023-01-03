import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib import animation
import matplotlib.patches as patches
import eulerN


mouse_location = [None, None] # inicijalizacija globalne promenljive - pozicija misa

def gui_mouse_move(event):
    global mouse_location
    mouse_location = [event.xdata, event.ydata]


def normalize(in_vector):
    magnitude = np.linalg.norm(in_vector, 2)
    if magnitude == np.inf or magnitude <= 0:
        out = [1, 0]
    else:
        out = in_vector/magnitude
    return out

world_size = [10.0, 10.0]  # [m]; dimenzije prostora

g = 9.81  # [m/s^2] gravitaciono ubrzanje
air_density = 1.225  # [kg/m^3] gustina vazduha
rubber_density = 1522  # [kg/m^3] gustina gume
drag_coefficient = 0.47  # koeficijent aerodinamicnosti sfera

# sfere
sphere_count = 25
r = (0.5 + np.random.rand(sphere_count)*0.5)*0.5  # [m] dimenzije sfera
A = r**2*np.pi  # [m^2] poprecni preseci sfera
m = rubber_density*4./3*r**3*np.pi  # [kg] mase (gumenih) sfera
v = np.zeros((sphere_count, 2))  # [m/s] trenutne brzine sfera
# [m] trenutni polozaji sfera
p = np.random.rand(sphere_count, 2)*0.5
p[:, 0] = (0.25 + p[:, 0])*world_size[0]
p[:, 1] = (0.75 + p[:, 1])*world_size[1]
colors = np.random.rand(sphere_count, 3)  # (R, G, B) boje sfera

# GUI
fig, ax = plt.subplots()
plt.axis((0, world_size[0], 0, world_size[1])) # ogranicavanje prikaza u okviru dimenzija prostora
ax.set_aspect('equal') # sprecavanje reskaliranja prikaza
plt.axis('off') # sakrivanje osa

# ivice
plt.plot([0, world_size[0]], [0, 0], c='k')
plt.plot([0, world_size[0]], [world_size[1], world_size[1]], c='k')
plt.plot([0, 0], [0, world_size[1]], c='k')
plt.plot([world_size[0], world_size[0]], [0, world_size[1]], c='k')

# sphere
spheres = []
for sphere in range(sphere_count):  # za svaku sferu(sphere)
    location = p[sphere, :]
    radius = r[sphere]
    diameter = 2*radius
    x = location[0] - radius
    y = location[1] - radius
    color = colors[sphere, :]
    spheres.append(plt.Circle((x, y), radius, facecolor=colors[sphere], edgecolor='black'))

# user force
r_user = min(world_size) * 0.2  # [m]
f_user = 15000  # [N = kg * m / s^2]
p_user = [-np.inf, -np.inf]
plt.connect('motion_notify_event', gui_mouse_move)  # registrovanje funkcije 


fps = 60  # broj osvezavanja prikaza u sekundi
time_scale = 1.0  # brzina simulacije
t1 = 0  # pocetni vremenski trenutak
dt = 1./fps  # vremenska razlika izmedju koraka

def init(): # inicijalizacija pocetnih pozicija
    for sphere in spheres:
        ax.add_patch(sphere)
    return spheres

# funkcija koja se poziva prilikom iscrtavanja svakog frame-a
def animate(t1):
    t2 = t1 + dt*time_scale  # naredni vremenski trenutak

    p_user = mouse_location  # čitanje vrednosti globalne promenljive
    # azuriranje polozaja i iscrtavanje
    for idx, sphere in enumerate(spheres):
        # sile
        # --------------------------------------------------------------
        F_weight = [0, -m[idx]*g]  # tezina tela (x, y)

        velocity = v[idx, :]
        F_drag = -velocity*np.linalg.norm(velocity, 2)*0.5*air_density*drag_coefficient*A[idx]  # otpor vazduha (x, y)

        F_user = [0, 0]
        try:
            direction = p[idx, :] - p_user
            if np.linalg.norm(direction, 2) <= r_user:
                F_user = normalize(direction)*f_user  # korisnicka sila (x, y)
        except:
            pass

        F = F_weight + F_drag + F_user

        # integracija
        # --------------------------------------------------------------
        ddpX = lambda t, p, v: F[0]/m[idx]  # p"(t) = F(t)/m) funkcija kretanja (x)
        ddpY = lambda t, p, v: F[1]/m[idx]  # p"(t) = F(t)/m) funkcija kretanja (y)
        _, pnX = eulerN.eulerN(t1, t2, t2 - t1, np.array([p[idx, 0], v[idx, 0]]), ddpX, 0.0)  # integracija (x)
        _, pnY = eulerN.eulerN(t1, t2, t2 - t1, np.array([p[idx, 1], v[idx, 1]]), ddpY, 0.0)  # integracija (y)
        p[idx, :] = [pnX[0, -1], pnY[0, -1]]  # trenutni polozaj
        v[idx, :] = [pnX[1, -1], pnY[1, -1]]  # trenutna brzina

        # prikaz
        # --------------------------------------------------------------
        location = p[idx, :]
        radius = r[idx]
        x = location[0] - radius
        y = location[1] - radius
        sphere.center = (x, y)
        ax.add_patch(sphere)

    return spheres

anim=animation.FuncAnimation(fig,animate,init_func=init,frames=20,interval=50,blit=True)

plt.show()
 
