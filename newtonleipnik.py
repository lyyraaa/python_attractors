import attractor
#http://www.3d-meier.de/tut19/Seite14.html
class NewtonLeipnik(attractor.Attractor):

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
