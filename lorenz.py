import attractor

class Lorenz(attractor.Attractor):

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
