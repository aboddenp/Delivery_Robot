# agentTop.py - Top Layer
# AIFCA Python3 code Version 0.7.9 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from agentMiddle import Rob_middle_layer
from agents import Environment

# my imports
import random
import time


class Rob_top_layer(Environment):
    def __init__(self, middle, timeout=200,mouse = False, locations={'mail': (-5, 10),
                                                       'o103': (50, 10), 'o109': (100, 10), 'storage': (101, 51)}):
        """middle is the middle layer
        timeout is the number of steps the middle layer goes before giving up
        locations is a loc:pos dictionary 
            where loc is a named location, and pos is an (x,y) position.
        """
        self.middle = middle
        self.timeout = timeout  # number of steps before the middle layer should give up
        self.locations = locations
        self.mouse = mouse
        self.mouse_pos = [None,None]
        if self.mouse != False:
            self.mouse = (random.randint(0,30), random.randint(0,30))
            self.update_mouse()
        self.current_named_location = ""


    def do(self, plan):
        """carry out actions.
        actions is of the form {'visit':list_of_locations}
        It visits the locations in turn.
        """
        to_do = plan['visit']
        for loc in to_do:
            self.current_named_location = loc
            self.update_mouse()
            position = self.locations[loc]
            arrived = self.middle.do({'go_to': position, 'timeout': self.timeout})
            if arrived == "moved":
                continue
            self.display(1, "Arrived at", loc, arrived)

    def update_mouse(self):
        if( self.mouse_pos[1] != None ):
            self.mouse_pos[0].set_visible(False)
            self.mouse_pos[1].set_visible(False)
        dx = random.randint(-10, 10)
        dy = random.randint(-10, 10)
        x = self.mouse[0] + dx
        y = self.mouse[1] + dy
        self.mouse_pos[0], = plt.plot([x], [y], "k<")
        self.mouse_pos[1] = plt.text(x + 1.0, y + 0.5, 'mouse')  # print the label above and to the right

    def proceed(self,current_location):
        self.update_mouse()
        # if the named location has moved notify the middle layer
        if current_location != self.locations[self.current_named_location]:
            # make middle layer work towards new location
            position = self.locations[self.current_named_location]
            arrived = self.middle.do({'go_to': position, 'timeout': self.timeout})
            self.display(1, "Arrived at", self.current_named_location, arrived)
            return False # alert middle layer not to proceed
        return True



import matplotlib.pyplot as plt


class Plot_env(object):
    def __init__(self, body, top):
        """sets up the plot
        """
        self.body = body
        plt.ion()
        plt.clf()
        plt.axes().set_aspect('equal')
        for wall in body.env.walls:
            ((x0, y0), (x1, y1)) = wall
            plt.plot([x0, x1], [y0, y1], "-k", linewidth=3)
        for loc in top.locations:
            (x, y) = top.locations[loc]
            plt.plot([x], [y], "k<")
            plt.text(x + 1.0, y + 0.5, loc)  # print the label above and to the right
        plt.plot([body.rob_x], [body.rob_y], "go")
        plt.draw()

    def plot_run(self):
        """plots the history after the agent has finished.
        This is typically only used if body.plotting==False
        """
        xs, ys = zip(*self.body.history)
        plt.plot(xs, ys, "go")
        wxs, wys = zip(*self.body.wall_history)
        plt.plot(wxs, wys, "ro")
        # plt.draw()


from agentEnv import Rob_body, Rob_env

env = Rob_env({((20, 0), (30, 20)), ((70, -5), (70, 25))})
body = Rob_body(env)
middle = Rob_middle_layer(body)
top = Rob_top_layer(middle, mouse=True)
middle.set_top(top)

# try:
pl = Plot_env(body, top)
top.do({'visit': ["mail", 'o109','o103']})

# You can directly control the middle layer:
# middle.do({'go_to':(30,20), 'timeout':200})
# Can you make it crash?

# Robot Trap for which the current controller cannot escape:
trap_env = Rob_env({((10, -21), (10, 0)), ((10, 10), (10, 31)), ((30, -10), (30, 0)),
                    ((30, 10), (30, 20)), ((50, -21), (50, 31)), ((10, -21), (50, -21)),
                    ((10, 0), (30, 0)), ((10, 10), (30, 10)), ((10, 31), (50, 31))})
trap_body = Rob_body(trap_env, init_pos=(-1, 0, 90))
trap_middle = Rob_middle_layer(trap_body)
trap_top = Rob_top_layer(trap_middle, locations={'goal': (71, 0)})

# Robot trap exercise:
# pl = Plot_env(trap_body, trap_top)
# trap_top.do({'visit': ['goal']})
