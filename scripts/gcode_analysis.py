# coding: utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def input_speed_reduce_time():
    num = input("Input speed reduce time [sec] >> ")
    try:
        num = float(num)
        print("wait_time is set to: {0}".format(num))
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
    plt.legend(loc="best")
    plt.draw()
    input_speed_reduce_time()

def plot_result():
    plt.title('Travel distance at each layer')
    plt.plot(Z,R)
    plt.xlabel('Z[mm]')
    plt.ylabel('travel distance[mm]')

df = pd.read_csv("out.csv",header=None)
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