import attractor
#http://www.3d-meier.de/tut19/Seite46.html
class Liuchen(attractor.Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 2.4
        self.b = -3.78
        self.c = 14
        self.d = -11
        self.e = 4
        self.f = 5.58
        self.g = -1

        self.dt = 0.002

    def step(self):
        deltax = self.dt * (self.a * self.y + self.b * self.x + self.c*self.y*self.z)
        deltay = self.dt * (self.d*self.y - self.z + self.e*self.x*self.z)
        deltaz = self.dt * (self.f*self.z + self.g*self.x*self.y)

        self.x += deltax
        self.y += deltay
        self.z += deltaz
