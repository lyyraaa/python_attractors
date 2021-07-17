import attractor
#http://www.3d-meier.de/tut19/Seite9.html
class Dequanli(attractor.Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 40
        self.c = 1.833
        self.d = 0.16
        self.e = 0.65
        self.k = 55
        self.f = 20

        self.dt = 0.001

    def step(self):
        deltax = self.dt * ( self.a*(self.y-self.x) + self.d * self.x * self.z)
        deltay = self.dt * (self.k * self.x + self.f *self.y - self.x * self.z)
        deltaz = self.dt * (self.c * self.z + self.x * self.y - self.e * self.x **2)

        self.x += deltax
        self.y += deltay
        self.z += deltaz
