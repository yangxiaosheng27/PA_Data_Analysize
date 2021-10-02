
import numpy as np 
x=[0,0.1]
y=[1,2]
x1=np.array(x)
y1=np.array(y)
 
import matplotlib.pyplot as plt 
 
fig=plt.figure()
 
ax1=fig.add_subplot(1,1,1)
plt.polar(x1,y1, '.-', alpha=0.5)

locs, labels = plt.yticks()
ticks = np.array(locs)
plt.yticks(ticks, (ticks - 2) * 10)
plt.grid('on')
plt.ion()
plt.draw()
plt.pause(0.001)

plt.ioff()
plt.show()