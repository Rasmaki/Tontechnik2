import scipy as sc
import numpy as np
import matplotlib.pyplot as plt
sample_rate = 44100
duration = 1
f = 5
samples = np.arange(duration*sample_rate)
t = samples / sample_rate
sin = sc.signal.square(2*np.pi*f*t)
sin_max = max(sin)
sin_eff = 1/len(sin)*sum(sin**2)
c = sin_max/sin_eff
print(c)


plt.plot(sin)
plt.show()