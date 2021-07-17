import attractor
#http://www.3d-meier.de/tut19/Seite3.html
class Aizawa(attractor.Attractor):

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
