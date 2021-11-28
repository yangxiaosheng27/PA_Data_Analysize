import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1,100,0.1)
y = x**2
z = x**3+5

plt.plot(x,y)
plt.show(block=False)      #绘制第一个图后阻塞程序

plt.plot(x,z)
plt.show(block=False)