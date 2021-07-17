import attractor
import math
#http://www.3d-meier.de/tut19/Seite41.html

class Thomas(attractor.Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.b = 0.19



        self.dt = 0.05

    def step(self):
        deltax = self.dt * (-1 * self.b * self.x + math.sin(self.y))
        deltay = self.dt * (-1 * self.b * self.y + math.sin(self.z))
        deltaz = self.dt * (-1 * self.b * self.z + math.sin(self.x))

        self.x += deltax
        self.y += deltay
        self.z += deltaz
