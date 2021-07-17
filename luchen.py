import attractor
import math
#https://www.hindawi.com/journals/complexity/2020/8315658/

class Luchen(attractor.Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        #self.x =
        #self.y =
        #self.z =
        self.x4 = 0.15
        self.x5 = 0.15

        self.phi = 1/0.026
        self.rho = 0.0000012
        self.c = 1.55

        #self.dt = 0.001

    def step(self):
        deltax = self.dt * (self.y - self.rho * math.sinh(self.phi * self.z))#(self.y - self.x)
        deltay = self.dt * (self.z - self.y)
        deltaz = self.dt * (self.x4)
        deltax4 = self.dt * (self.x5)
        deltax5 = self.dt * (-1 * self.c * self.x5 - self.rho * math.sinh(self.phi * self.x4) - 5 * self.z - 5 * self.y - 0.1 * self.x)

        self.x += deltax
        self.y += deltay
        self.z += deltaz
        self.x4 += deltax4
        self.x5 += deltax5
