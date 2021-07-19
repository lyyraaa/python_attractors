# code from https://www.youtube.com/watch?v=Hqg4qePJV2U
# Pyglet OpenGL tutorial by DLC ENERGY
# As taught by Aiden Ward
#https://github.com/jjstrydom/pyglet_examples/blob/master/textured_square.py

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
import random
from attractor import Lorenz,Rossler,Liuchen,Thomas,NewtonLeipnik,Halvorsen,Dequanli,Aizawa
import argparse
import sys


class Model:

    def update(self,dt):
        if self.step < self.lim_per_att*3:
            self.step += 3
        else:
            self.step = 3
        for att in range(self.attC):
            self.attractor_list[att].step()
            self.point_list[att][self.step-3:self.step] = [self.scale * x for x in self.attractor_list[att].get_location()]
            self.line_list[att].vertices = self.point_list[att][self.step:]+self.point_list[att][:self.step]

    def __init__(self,attractortype,attC,scale,fps,limit,dt):

        self.attractortype = attractortype
        self.limit = limit
        self.attC = attC
        self.lim_per_att = int(self.limit/self.attC)
        self.scale = scale
        self.fps = fps
        self.dt = dt

        self.attractor_list = []
        self.line_list = []
        self.point_list = []

        for att in range(self.attC):

            x,y,z = random.random()*0.03,random.random()*0.03,random.random()*0.03


            if attractortype == "LORENZ":
                self.attractor_list.append(Lorenz(x,y,z,self.dt))
            elif attractortype == "ROSSLER":
                self.attractor_list.append(Rossler(x,y,z,self.dt))
            elif attractortype == "LIUCHEN":
                self.attractor_list.append(Liuchen(x,y,z,self.dt))
            elif attractortype == "THOMAS":
                self.attractor_list.append(Thomas(x,y,z,self.dt))
            elif attractortype == "NEWTONLEIPNIK":
                self.attractor_list.append(NewtonLeipnik(x,y,z,self.dt))
            elif attractortype == "HALVORSEN":
                self.attractor_list.append(Halvorsen(x,y,z,self.dt))
            elif attractortype == "DEQUANLI":
                self.attractor_list.append(Dequanli(x,y,z,self.dt))
            elif attractortype == "AIZAWA":
                self.attractor_list.append(Aizawa(x,y,z,self.dt))
            else:
                print("Attractor type not recognised")
                sys.exit(0)


            self.line_list.append(pyglet.graphics.vertex_list(self.lim_per_att, 'v3f/stream', 'c4B/static'))#c3B/static
            self.point_list.append([0,0,0]*self.lim_per_att)
            self.point_list[att][:3] = (x,y,z)

            mult = 0.5 * (att+1)/(attC*0.7)
            baser,baseg,baseb = 255,255,255#255,51,218

            self.color_list = []
            for place in range(1,self.lim_per_att+1):
                self.color_list.append(baser)
                self.color_list.append(baseg)
                self.color_list.append(baseb)
                self.color_list.append(int(255*(place/self.lim_per_att)))

            self.line_list[att].colors = self.color_list
            self.line_list[att].vertices[:3] = [x,y,z]

        self.step = 3

        pyglet.clock.schedule_interval(self.update, 1.0/self.fps)

        #else:
        #    pass

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

    def __init__(self, arglist,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        arglist = vars(arglist)

        self.model = Model(
            attractortype = arglist.get("attractor")[0],
            attC = arglist.get("points")[0],
            scale= arglist.get("scale")[0],
            fps = arglist.get("framerate")[0],
            limit = arglist.get("limit")[0],
            dt = arglist.get("timestep")[0])

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

    parser = argparse.ArgumentParser(description="Draws some chaotic attractors and dynamical systems")

    parser.add_argument("attractor", metavar='A', type=str, nargs=1,
        help="the attractor/system to draw, choose from:\
        [LORENZ | \
        AIZAWA | \
        CHENLEE | \
        DEQUANLI | \
        HALVORSEN | \
        JOURNAL | \
        LIUCHEN | \
        NEWTONLEIPNIK | \
        POLYNOMIAL_A | \
        ROSSLER | \
        THOMAS]")
    parser.add_argument("-p","--points",nargs=1,type=int,default=[10],
        help="the number of points to draw, default 10")
    parser.add_argument("-s","--scale",nargs=1,type=int,default=[1],
        help="scale factor for size of drawing, default 1")
    parser.add_argument("-dt","--timestep",nargs=1,type=float,default=[0.01],
        help="timestep for calculations; delta t, default 0.01")
    parser.add_argument("-l","--limit",nargs=1,type=int,default=[30000],
        help="limit of number of points to draw, affects length of trails, default 30k")
    parser.add_argument("-fps","--framerate",nargs=1,type=int,default=[60],
        help="framerate to process at, default 60")
    args = parser.parse_args()


    window = Window(width=400, height=300, caption='My caption',resizable=True,arglist=args)

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0,0,0,1)
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()
