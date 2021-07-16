# code from https://www.youtube.com/watch?v=Hqg4qePJV2U
# Pyglet OpenGL tutorial by DLC ENERGY
# As taught by Aiden Ward
#https://github.com/jjstrydom/pyglet_examples/blob/master/textured_square.py

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
import random
from lorenz import Lorenz
import sys


class Model:

    def reset(self):
        for att in range(self.attC):
            self.line_list[att].vertices = [0,0,0]*self.lim_per_att
            self.line_list[att].vertices[:3] = self.attractor_list[att].get_location()

    def update(self,dt):
        if self.step < self.lim_per_att:
            self.step += 3
            for att in range(self.attC):
                self.attractor_list[att].step()
                self.line_list[att].vertices[self.step-3:self.step] = self.attractor_list[att].get_location()
        else:
            self.reset()
            self.step = 3



    def __init__(self,attractortype="LORENZ",attC = 10):

        self.limit = 10000
        self.attC = attC
        self.lim_per_att = int(self.limit/self.attC)

        if attractortype == "LORENZ":

            self.attractor_list = []
            self.line_list = []
            for att in range(self.attC):

                x,y,z = random.random()*0.03,random.random()*0.03,random.random()*0.03

                self.attractor_list.append(Lorenz(x,y,z,0.01))


                self.line_list.append(pyglet.graphics.vertex_list(self.lim_per_att, 'v3f/stream', 'c3B/static'))

                mult = 0.5 * (att+1)/(attC*0.7)
                baser,baseg,baseb = 255,51,218
                self.line_list[att].colors = (int(baser*mult), int(baseg*mult), int(baseg*mult)) * self.lim_per_att
                #[random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)]*self.lim_per_att
                self.line_list[att].vertices[:3] = [x,y,z]

            self.step = 3

            pyglet.clock.schedule_interval(self.update, 1.0/60)

        else:
            pass

    def draw(self):
        for att in range(self.attC):
            self.line_list[att].draw(pyglet.gl.GL_LINE_STRIP)


class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self, dx, dy):
        dx/= 8
        dy/= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update(self,dt,keys):
        sens = 0.4
        s = dt*10
        #shiftmod = keys[key.LSHIFT] * 1.5 * sens
        rotY = -self.rot[1]/180*math.pi
        dx, dz = math.sin(rotY), math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx*sens
            self.pos[2] -= dz*sens
        if keys[key.S]:
            self.pos[0] -= dx*sens
            self.pos[2] += dz*sens
        if keys[key.A]:
            self.pos[0] -= dz*sens
            self.pos[2] -= dx*sens
        if keys[key.D]:
            self.pos[0] += dz*sens
            self.pos[2] += dx*sens
        if keys[key.SPACE]:
            self.pos[1] += s*sens
        if keys[key.LCTRL]:
            self.pos[1] -= s*sens

class Window(pyglet.window.Window):

    def push(self,pos,rot):
        glPushMatrix()
        rot = self.player.rot
        pos = self.player.pos
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.model = Model()
        self.player = Player((0.5,1.5,1.5),(-30,0))

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self, KEY, _MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        self.model.draw()
        glPopMatrix()

if __name__ == '__main__':
    window = Window(width=400, height=300, caption='My caption',resizable=True)
    glClearColor(0,0,0,1)
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()
