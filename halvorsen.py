import attractor
#http://www.3d-meier.de/tut19/Seite13.html
class Halvorsen(attractor.Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 1.4

        self.dt = 0.005

    def step(self):
        deltax = self.dt * (-1 * self.a * self.x - 4 * self.y - 4*self.z - self.y**2)
        deltay = self.dt * (-1 * self.a * self.y - 4 * self.z - 4*self.x - self.z**2)
        deltaz = self.dt * (-1 * self.a * self.z - 4 * self.x - 4*self.y - self.x**2)

        self.x += deltax
        self.y += deltay
        self.z += deltaz
