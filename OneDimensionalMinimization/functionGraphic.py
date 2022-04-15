import matplotlib.pyplot as plt
from math import pow 
import numpy as np

x = np.arange(1.5, 2, 0.01)
y = [pow(x, 4) + 8 * pow(x, 3) - 6 * pow(x, 2) - 72 * x + 90 for x in x]
plt.plot(x, y)
plt.show()