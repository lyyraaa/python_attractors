import attractor
#http://www.3d-meier.de/tut19/Seite8.html
class Chenlee(attractor.Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 5
        self.b = -10
        self.c = -0.38

        self.dt = 0.004


    def step(self):
        deltax = self.dt * (self.a * self.x - self.y * self.z)
        deltay = self.dt * (self.b * self.y + self.x * self.z)
        deltaz = self.dt * (self.c * self.z + self.x * (self.y/3.0))

        self.x += deltax
        self.y += deltay
        self.z += deltaz
