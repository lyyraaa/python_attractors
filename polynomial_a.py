import attractor
#http://www.3d-meier.de/tut19/Seite64.html
class Polynomial_A(attractor.Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.p0 = 1.586
        self.p1 = 1.124
        self.p2 = 0.281

        self.dt = 0.001

    def step(self):
        deltax = self.dt * (self.p0 + self.y - self.y*self.z)
        deltay = self.dt * (self.p1 + self.z - self.x * self.z)
        deltaz = self.dt * (self.p2 + self.x - self.x*self.y)

        self.x += deltax
        self.y += deltay
        self.z += deltaz
