import attractor

class Rossler(attractor.Attractor):

    def __init__(self,x,y,z,dt):
        super().__init__(x,y,z,dt)

        self.a = 0.1
        self.b = 0.1
        self.c = 14

        self.dt = 0.03


    def step(self):
        deltax = self.dt * (-self.y - self.z)
        deltay = self.dt * (self.x + self.a * self.y)
        deltaz = self.dt * (self.b + self.z * (self.x - self.c))

        self.x += deltax
        self.y += deltay
        self.z += deltaz
