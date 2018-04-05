import numpy as np
import pylab
import matplotlib.pyplot as plt


def onclick(event):
    print('event.button={0},  event.x={1}, event.y={2}, event.xdata={3}, event.ydata={4}'.format(event.button, event.x, event.y, event.xdata, event.ydata))

fig=plt.figure()
ax=fig.add_subplot(111)
x,y = 1,1
ax.plot(x,y,'ro')
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
