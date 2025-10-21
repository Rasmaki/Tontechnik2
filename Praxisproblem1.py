import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


fs = sd.query_devices(sd.default.device, 'output')['default_samplerate']
dur = 1 # Dauer
ydb = np.arange(0, 105, 5)
y = (10**(ydb/10))/10000000000
t = np.arange(dur * fs) / fs
f = [125, 250, 500, 1000, 2000, 4000, 8000]  # Frequenzen
ydb_temp = []
noise = np.ones(len(t))

def play_sin(test_state):
    global y, noise, f, t
    for j in range(len(f)):
        for i in range(len(y)):
            if test_state:
                noise = np.random.normal(0, 0.2, len(t))
            x =  y[i] * np.sin(2 * np.pi * f[j] * t)*noise[i]
            sd.play(x, fs)
            sd.wait()
            usr_input =input("Haben Sie den Ton gehört? Y/N...")
            if usr_input == 'y':
                print("Deine Hörschwelle bei {1} Hz ist {0} dB".format(ydb[i], f[j]))
                ydb_temp.append(ydb[i])
                break
    return ydb_temp


print("Linkes Ohr:")
ydb_l = play_sin(True)
print("Rechtes Ohr:")
ydb_r = play_sin(False)
print("Linkes Ohr mit verdeckung:")
ydb_r_n = play_sin(True)
print("Rechtes Ohr mit verdeckung:")
ydb_l_n = play_sin(True)

plt.figure()
plt.plot(f, ydb_l, label='Linkes Ohr')
plt.plot(f, ydb_r, label='Rechtes Ohr')
plt.xscale('log')
plt.legend()
plt.title('Hörschwelle relativ zu 1kHz')
plt.xlabel('Frequenz (Hz)')
plt.ylabel('Hörschwelle (dB)')
plt.grid()
plt.show()
