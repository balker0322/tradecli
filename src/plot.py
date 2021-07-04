from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from collections import deque as dq
from random import random

# plt.style.use('fivethirtyeight')

class AnimatePlot():

    def __init__(self):
        self.y_vals = []
        self.range = 1000
        self.x_vals = []
        for i in range(int(self.range)):
            self.x_vals.append(i)
            self.y_vals.append(None)
        self.num = None
        self.label = 'Price'
        self.markers = []
    
    def add_marker(self, marker):
        self.markers.append(marker)
    
    def clear_markers(self):
        self.markers = []

    def set_label(self, label):
        self.label = label

    def animate(self, i):
        print(i)
        # self.set_y_vals()
        x = np.array(self.x_vals)
        y1 = np.array(self.y_vals)

        plt.cla()

        plt.plot(x, y1, label=self.label)

        if self.num is not None:
            y_mark = []
            for _ in range(self.range):
                y_mark.append(self.num)
            plt.plot(x, np.array(y_mark), label='{0:.4f} USDT'.format(self.num))
        
        if self.markers:
            for marker in self.markers:
                y_marker = []
                for _ in range(self.range):
                    y_marker.append(marker['value'])
                plt.plot(x, np.array(y_marker), label=marker['label'])

        plt.xlim(0, self.range)

        plt.legend(loc='upper left')
        plt.tight_layout()

    def start_plot(self):
        self.ani = FuncAnimation(plt.gcf(), self.animate, interval=1)
        plt.tight_layout()
        plt.show()

    def append_y_vals(self, new_val):
        self.num = new_val
        print('new_val: {}'.format(self.num))
        self.y_vals.append(self.num)
        if len(self.y_vals)>self.range:
            array_size = int(-1*self.range)
            self.y_vals = self.y_vals[array_size:]