#!/usr/bin/env python

import re
import sys
import pdb

class MyClass():
  def __init__(self):
    self.LASER_REDUCTION_RATE = 0.8
    self.THRESHOLD = 10e8

m = MyClass()    

if len(sys.argv)<2:
    print("Convert error: specify file")
    exit()

g0pattern = r"^G0.*"
g1pattern = r"^G1.*"
g0re = re.compile(g0pattern)
g1re = re.compile(g1pattern)

Xpattern = r".*X[-\.\d]+"
Ypattern = r".*Y[-\.\d]+"
Zpattern = r".*Z[-\.\d]+"
Spattern = r".*S\d+"
Xre = re.compile(Xpattern)
Yre = re.compile(Ypattern)
Zre = re.compile(Zpattern)
Sre = re.compile(Spattern)

filepath = sys.argv[1]
filename = filepath.split('/')[-1]

##########################################################################
## extrace coordinate from gcode -> generate out.csv
##########################################################################
currentX = 0
currentY = 0
currentZ = 0
currentS = 0

TMP_CSV_FOLDER = "./tmp/out.csv"
fout = open(TMP_CSV_FOLDER,'w')
should_update = False

with open(filepath) as f:
    lines = f.readlines()
    for line in lines:
        if g0re.match(line):
            if Zre.match(line):
                should_update = True
                nextZ = re.findall(Zpattern,line)[0].split('Z')[1]
                if currentZ != nextZ:
                    currentZ = nextZ
        elif g1re.match(line):
            if Xre.match(line): 
                should_update = True
                nextX = re.findall(Xpattern,line)[0].split('X')[1]
                if currentX != nextX:
                    currentX = nextX
            if Yre.match(line): 
                should_update = True
                nextY = re.findall(Ypattern,line)[0].split('Y')[1]
                if currentY != nextY:
                    currentY = nextY
            if Zre.match(line):
                should_update = True
                nextZ = re.findall(Zpattern,line)[0].split('Z')[1]
                if currentZ != nextZ:
                    currentZ = nextZ
            # if Sre.match(line):
            #     nextS = re.findall(Spattern,line)[0].split('S')[1]
            #     if currentS != nextS:
            #         currentS = nextS
            # should_update = should_update and (float(currentS) > 0)
            if should_update:
                # fout.write("{0},{1},{2},{3}\n".format(currentX,currentY,currentZ,currentS))
                fout.write("{0},{1},{2}\n".format(currentX,currentY,currentZ))
                should_update = False
fout.close() 

##########################################################################
## Visualize gcode detail and decide threshold
##########################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def input_reduce_rate():
    VERSION = sys.version.split(' ')[0].split('.')[0]
    if VERSION=='2':
        num = raw_input("Input reduce rate [%] (default: 80) >> ")
    elif VERSION=='3':
        num = input("Input reduce rate [%] (default: 80) >> ")
    else:    
        print("Invalid python version.")
        exit()
    if num=="":
      num = 80
    try:
        num = int(num)
        m.LASER_REDUCTION_RATE = float(num / 100.0)
        print("speed rate is set to: {0}[%]".format(num))
        plt.close()
    except ValueError:
        print("Not a float number")
        exit()

def onclick(event):
    # print('event.button={0},  event.x={1}, event.y={2}, event.xdata={3}, event.ydata={4}'.format(event.button, event.x, event.y, event.xdata, event.ydata))
    r = event.ydata 
    plot_result()
    xmin, xmax = plt.xlim()
    plt.plot([xmin+abs(xmin)*1.1,xmax*0.9],[r,r],'r-',label="threshold: {0:.1f}mm".format(r))
    print("threshold is set as {0} mm".format(r))
    m.THRESHOLD = r
    plt.legend(loc="best")
    plt.draw()
    input_reduce_rate()

def plot_result():
    plt.title('Travel distance at each layer')
    plt.plot(Z,R)
    plt.xlabel('Z[mm]')
    plt.ylabel('travel distance[mm]')

df = pd.read_csv(TMP_CSV_FOLDER,header=None)
X = df.values[:,0]
Y = df.values[:,1]
Z = df.values[:,2]
#plt.scatter(X,Y,s=50,c=Z)
dX = (np.diff(X))
dY = (np.diff(Y))
travel = pd.DataFrame({'r':np.sqrt(np.square(dX)+np.square(dY)),'Z':Z[1:]})
Z = np.array(travel.groupby('Z').sum().r.index)
R = travel.groupby('Z').sum().values

plot_result()
cid = plt.gcf().canvas.mpl_connect('button_press_event',onclick)
plt.draw()

plt.show()

##########################################################################
## Obtain Z height lists to reduce speed filter 
##########################################################################

import numpy as np
import pandas as pd
df = pd.read_csv(TMP_CSV_FOLDER,header=None)
X = df.values[:,0]
Y = df.values[:,1]
Z = df.values[:,2]
dX = (np.diff(X))
dY = (np.diff(Y))
travel = pd.DataFrame({'r':np.sqrt(np.square(dX)+np.square(dY)),'Z':Z[1:]})
original = travel.groupby('Z').sum() 
z_filter_list = np.array(original[original['r']<m.THRESHOLD].index)
print(z_filter_list)

##########################################################################
## overwrite laser speed
##########################################################################

currentX = 0
currentY = 0
currentZ = 0
currentS = 0
fout = open("./converted/"+filename,'w')

print("threshold",m.THRESHOLD)
print("reduction rate",m.LASER_REDUCTION_RATE)
with open(filepath) as f:
    lines = f.readlines()
    for line in lines:
        if g0re.match(line):
            if Zre.match(line):
                should_update = True
                nextZ = re.findall(Zpattern,line)[0].split('Z')[1]
                if currentZ != nextZ:
                    currentZ = nextZ
        elif g1re.match(line):
            if Xre.match(line): 
                should_update = True
                nextX = float(re.findall(Xpattern,line)[0].split('X')[1])
                if currentX != nextX:
                    currentX = nextX
            if Yre.match(line): 
                should_update = True
                nextY = float(re.findall(Ypattern,line)[0].split('Y')[1])
                if currentY != nextY:
                    currentY = nextY
            if Zre.match(line):
                should_update = True
                nextZ = float(re.findall(Zpattern,line)[0].split('Z')[1])
                if currentZ != nextZ:
                    currentZ = nextZ
            if Sre.match(line):
                nextS = int(re.findall(Spattern,line)[0].split('S')[1])
                if currentS != nextS:
                    currentS = nextS
            if float(currentZ) in z_filter_list:
                if Sre.match(line):
                    updateS = int(currentS * m.LASER_REDUCTION_RATE)
                    if updateS < 1:
                        updateS = 1
                    line = re.sub(r"S\d+","S"+str(updateS),line)    
        fout.write(line)            
fout.close() 

print('convert process done.')
