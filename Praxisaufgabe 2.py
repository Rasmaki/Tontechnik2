import scipy as sc
import numpy as np
import matplotlib.pyplot as plt
sample_rate = 44100
duration = 2
f = 100
samples = np.arange(duration*sample_rate)
t = samples / sample_rate


def calc(sig1):
    c = max(sig1) / (np.sqrt(1 / len(sig1) * sum(sig1 ** 2)))
    return c


sin = np.sin(2*np.pi*f*t)
tri = sc.signal.sawtooth(2*np.pi*f*t, width=0.5)
saw = sc.signal.sawtooth(2*np.pi*f*t)
rect = sc.signal.square(2*np.pi*f*t)

sol = [calc(sin), calc(tri), calc(saw), calc(rect)]
print("Scheitelfaktor Sinus:",round(sol[0], 2))
print("Scheitelfaktor Dreieck:",round(sol[1], 2))
print("Scheitelfaktor Sägezahn:",round(sol[2], 2))
print("Scheitelfaktor Rechteck:",round(sol[3], 2))
