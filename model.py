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

import pyglet_gui
from pyglet_gui.theme import Theme
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton
from pyglet_gui.containers import VerticalContainer, HorizontalContainer, Spacer
from pyglet_gui.sliders import HorizontalSlider
from pyglet_gui.gui import Label


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


            self.line_list.append(pyglet.graphics.vertex_list(self.lim_per_att, 'v3f/stream', 'c4B/dynamic'))#c3B/static
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

    def get_limperat(self):
        return self.lim_per_att

    def change_col(self,col_list):
        self.color_list = col_list
        for att in range(self.attC):
            self.line_list[att].colors = self.color_list


class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.initpos = list(pos)
        self.initrot = list(rot)

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

    def reset(self):
        self.pos = self.initpos[:]
        self.rot = self.initrot[:]

    def getPos(self):
        return self.pos

    def getRot(self):
        return self.rot

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
        gluPerspective(self.fov, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    def set_fov(self,fov):
        self.fov = fov

    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self, arglist,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)
        self.fov=70

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

    def getPlayer(self):
        return self.player

class WindowUI(pyglet.window.Window):

    def __init__(self, window3D, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window3D = window3D

        self.batch = pyglet.graphics.Batch()

        self.theme = Theme(
            {"font": "Lucida Grande",
            "font_size": 12,
            "text_color": [255, 255, 255, 255],
            "gui_color": [255, 255, 255, 255],
            "button": {
                "text_color": [0, 0, 0, 255],
                "down": {
                    "image": {
                        "source": "button-down.png",
                        "frame": [8, 6, 2, 2],
                        "padding": [18, 18, 8, 6]
                        },
                    },
                "up": {
                    "image": {
                        "source": "button.png",
                        "frame": [6, 5, 6, 3],
                        "padding": [18, 18, 8, 6]
                        }
                    }
                },
            "slider": {
                   "knob": {
                       "image": {
                           "source": "slider-knob.png"
                       },
                       "offset": [-5, -11]
                   },
                   "padding": [8, 8, 8, 8],
                   "step": {
                       "image": {
                           "source": "slider-step.png"
                       },
                       "offset": [-2, -8]
                   },
                   "bar": {
                       "image": {
                           "source": "slider-bar.png",
                           "frame": [8, 8, 8, 0],
                           "padding": [8, 8, 8, 8]
                       }
                   }
               }
            }, resources_path='theme/')

        label_fov = Label('Change FOV')
        label_col = Label('Change Colour')
        label_position = Label('Player position\nand view angle')
        self.label_pos = Label('postionsplaceholder')
        self.label_rot = Label('rotationplaceholder')

        button_reset = OneTimeButton('RESET POS', on_release=self.callback)
        # FOR TOGGLE BUTTONS USE Button not OneTimeButton, and on_release -> on_press

        button_col = OneTimeButton('CHANGE COL', on_release=self.change_col)


        self.sliderFOV = HorizontalSlider(on_set=self.change_fov)

        self.sliderR = HorizontalSlider()
        self.sliderG = HorizontalSlider()
        self.sliderB = HorizontalSlider()

        container_pos = VerticalContainer([label_position, self.label_pos, self.label_rot])
        container_fov = VerticalContainer([label_fov, self.sliderFOV, button_reset])
        container_col = VerticalContainer([label_col, self.sliderR, self.sliderG, self.sliderB, button_col])

        self.manager = Manager(\
            content=HorizontalContainer([Spacer(10),container_pos, Spacer(25),container_fov, Spacer(25), container_col]),
            window=self,
            theme=self.theme,
            batch=self.batch,
            is_movable=False)


    def on_draw(self):
        self.clear()
        self.batch.draw()

        self.update_labels()


    def update_labels(self):
        posinfo = ["{:.2f}".format(s) for s in self.window3D.player.getPos()]
        rotinfo = ["{:.2f}".format(s) for s in self.window3D.player.getRot()]
        self.label_pos.set_text("x: " + posinfo[0] + " y: " + posinfo[1] + " z: " + posinfo[2])
        self.label_rot.set_text("V: " + rotinfo[0] + " H: " + rotinfo[1])

    def callback(self,is_pressed):
        self.window3D.set_fov(75)
        self.window3D.getPlayer().reset()

    def change_col(self,is_pressed):
        limp = self.window3D.model.get_limperat()
        r,g,b = int(255*self.sliderR.value),int(255*self.sliderG.value),int(255*self.sliderB.value)
        col_list = []
        for place in range(1,limp+1):
            col_list.append(r)
            col_list.append(g)
            col_list.append(b)
            col_list.append(int(255*(place/limp)))

        self.window3D.model.change_col(col_list)

    def change_fov(self,is_pressed):
        self.window3D.set_fov(int(65 + self.sliderFOV.value*45))

    def on_close(self):
        self.window3D.close()
        self.close()




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


    window = Window(width=600, height=450, caption='My caption',resizable=True,arglist=args)


    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0,0,0,1)
    glEnable(GL_DEPTH_TEST)

    windowUI = WindowUI(window,width=1000, height=400, caption='UI',resizable=True)
    pyglet.app.run()
