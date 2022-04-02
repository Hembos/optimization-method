import matplotlib.pyplot as plt
from math import sin, cos
import numpy as np

x = np.arange(-5, -4, 0.01)
y = [x * sin(x) + 2 * cos(x) for x in x]
plt.plot(x, y)
plt.show()