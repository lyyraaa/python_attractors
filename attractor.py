import math

class Attractor:

    def __init__(self,x,y,z,dt):
        self.x = x
        self.y = y
        self.z = z

        self.dx = 0
        self.dy = 0
        self.dz = 0

        self.dt = dt

    def get_location(self):
        return (self.x,self.y,self.z)

    def get_velocity(self):
        return (self.dx,self.dy,self.dz)


#https://en.wikipedia.org/wiki/Lorenz_system
class Lorenz(Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.rho = 28
        self.beta = 8/3
        self.sigma = 10


    def step(self):
        deltax = self.dt * (self.sigma * (self.y-self.x))
        deltay = self.dt * (self.x * (self.rho - self.z) - self.y)
        deltaz = self.dt * (self.x * self.y - self.beta * self.z)

        self.x += deltax
        self.y += deltay
        self.z += deltaz


#http://www.3d-meier.de/tut19/Seite14.html
class NewtonLeipnik(Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 0.4
        self.b = 0.175

    def step(self):
        deltax = self.dt * (-1 * self.a * self.x + self.y + 10*self.y*self.z)
        deltay = self.dt * (-1 * self.x - 0.4 * self.y + 5 * self.x * self.z)
        deltaz = self.dt * (self.b * self.z - 5* self.x* self.y)

        self.x += deltax
        self.y += deltay
        self.z += deltaz

#https://en.wikipedia.org/wiki/R%C3%B6ssler_attractor
class Rossler(Attractor):

    def __init__(self,x,y,z,dt=0.03):
        super().__init__(x,y,z,dt)

        self.a = 0.1
        self.b = 0.1
        self.c = 14


    def step(self):
        deltax = self.dt * (-self.y - self.z)
        deltay = self.dt * (self.x + self.a * self.y)
        deltaz = self.dt * (self.b + self.z * (self.x - self.c))

        self.x += deltax
        self.y += deltay
        self.z += deltaz

#http://www.3d-meier.de/tut19/Seite41.html
class Thomas(Attractor):

    def __init__(self,x,y,z,dt=0.05):
        super().__init__(x,y,z,dt)
        self.b = 0.19

    def step(self):
        deltax = self.dt * (-1 * self.b * self.x + math.sin(self.y))
        deltay = self.dt * (-1 * self.b * self.y + math.sin(self.z))
        deltaz = self.dt * (-1 * self.b * self.z + math.sin(self.x))

        self.x += deltax
        self.y += deltay
        self.z += deltaz

#http://www.3d-meier.de/tut19/Seite3.html
class Aizawa(Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 0.95
        self.b = 0.7
        self.c = 0.6
        self.d = 3.5
        self.e = 0.25
        self.f = 0.1

    def step(self):
        deltax = self.dt * (self.x * (self.z - self.b) - self.d * self.y)
        deltay = self.dt * (self.d * self.x + (self.z-self.b)*self.y)
        deltaz = self.dt * (self.c + self.a * self.z - (1/3)*self.z**3 - (self.x**2 + self.y**2)*(1+self.e*self.z) + self.f * self.z * self.x **3)

        self.x += deltax
        self.y += deltay
        self.z += deltaz

#http://www.3d-meier.de/tut19/Seite9.html
class Dequanli(Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 40
        self.c = 1.833
        self.d = 0.16
        self.e = 0.65
        self.k = 55
        self.f = 20

    def step(self):
        deltax = self.dt * ( self.a*(self.y-self.x) + self.d * self.x * self.z)
        deltay = self.dt * (self.k * self.x + self.f *self.y - self.x * self.z)
        deltaz = self.dt * (self.c * self.z + self.x * self.y - self.e * self.x **2)

        self.x += deltax
        self.y += deltay
        self.z += deltaz

#http://www.3d-meier.de/tut19/Seite13.html
class Halvorsen(Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 1.4
        self.y = 0
        self.z = 0

    def step(self):
        deltax = self.dt * (-1 * self.a * self.x - 4 * self.y - 4*self.z - self.y**2)
        deltay = self.dt * (-1 * self.a * self.y - 4 * self.z - 4*self.x - self.z**2)
        deltaz = self.dt * (-1 * self.a * self.z - 4 * self.x - 4*self.y - self.x**2)

        self.x += deltax
        self.y += deltay
        self.z += deltaz

#http://www.3d-meier.de/tut19/Seite46.html
class Liuchen(Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 2.4
        self.b = -3.78
        self.c = 14
        self.d = -11
        self.e = 4
        self.f = 5.58
        self.g = -1

    def step(self):
        deltax = self.dt * (self.a * self.y + self.b * self.x + self.c*self.y*self.z)
        deltay = self.dt * (self.d*self.y - self.z + self.e*self.x*self.z)
        deltaz = self.dt * (self.f*self.z + self.g*self.x*self.y)

        self.x += deltax
        self.y += deltay
        self.z += deltaz
