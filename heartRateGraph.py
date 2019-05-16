
import serial, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
from matplotlib.lines import Line2D 


ser = serial.Serial('/dev/cu.usbmodem1411', 250000)

s1y = []
s2y = []
s1x = []
s2x = []
s1y.append(0)
s2y.append(0)
s1x.append(0)
s2x.append(0)

def update_line():
   data = ser.readline().decode()
   if len(data) > 7:
      sensorList = data.split(',')
      sensor1 = float(sensorList[0])
      sensor2 = float(sensorList[1])
      sensor2 = sensor2/4
      s1y.append(sensor1)
      s2y.append(sensor2)
      s1x.append(len(s1y))
      s2x.append(len(s2y))
   else: 
      data = ser.readline().decode()
      sensorList = data.split(',')
      sensor1 = float(sensorList[0])
      sensor2 = float(sensorList[1])
      sensor2 = sensor2/4
      s1y.append(sensor1)
      s2y.append(sensor2)
      s1x.append(len(s1y))
      s2x.append(len(s2y))
   return s1x, s1y, s2x, s2y


def data_gen():
    while True:
        yield update_line()

def run(data):
   s1x, s1y, s2x, s2y = data
   ax1.set_xlim(0, max(s1x)+20)
   ax2.set_xlim(0, max(s2x)+20)
   ax1.set_ylim(min(s1y), max(s1y)+50)
   ax2.set_ylim(min(s2y), max(s2y)+50)
   line1.set_data(s1x, s1y)
   line2.set_data(s2x, s2y)
   return line1, line2


fig = plt.figure()

ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ax1.set_title('Sensor 1')
ax1.set_xlabel('Seconds since starting')
ax1.set_ylabel('BPM')
 
ax2.set_title('Sensor 2')
ax2.set_xlabel('Seconds since starting')
ax2.set_ylabel('BPM')

line1 = Line2D([], [], color='red')
line2 = Line2D([], [], color='blue')

ax1.add_line(line1)
ax2.add_line(line2)


line_ani = animation.FuncAnimation(fig, run, data_gen)

plt.tight_layout()
plt.show()
