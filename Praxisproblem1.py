import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import threading


fs = sd.query_devices(sd.default.device, 'output')['default_samplerate']
dur = 1 # Dauer
ydb = np.arange(40, 105, 5)
y = (10**(ydb/10))/10000000000
t = np.arange(dur * fs) / fs
f = [125, 250, 500, 1000, 2000, 4000, 8000]  # Frequenzen


def play_sin(ch):
    global y, f, t
    ydb_temp = []
    for j in range(len(f)):
        for i in range(len(y)):
            x =  y[i] * np.sin(2 * np.pi * f[j] * t)
            sd.play(x, fs, mapping=[ch])
            sd.wait()
            usr_input =input("Haben Sie den Ton gehört? Y/N...")
            if usr_input == 'y':
                print("Deine Hörschwelle bei {1} Hz ist {0} dB".format(ydb[i], f[j]))
                ydb_temp.append(ydb[i])
                break
    return ydb_temp


def play_noise(rms=0.0001):
    global t

    stop_event = threading.Event()

    def callback(outdata, frames, time, status):
        if status:
            pass
        noise = np.random.normal(0, 1.0, size=(frames, 1)).astype(np.float32)
        cur_rms = np.sqrt(np.mean(noise**2))
        noise *= (rms/cur_rms)
        outdata[:] = noise

    noise_stream = sd.OutputStream(channels=1, callback=callback, samplerate=fs)
    noise_stream.start()

    try:
        stop_event.wait()
    finally:
        noise_stream.stop()
        noise_stream.close()

    return stop_event


print("Linkes Ohr:")
ydb_l = play_sin(1)
print("Rechtes Ohr:")
ydb_r = play_sin(2)
threading.Thread(target=play_noise, daemon=True).start()
print("Linkes Ohr mit verdeckung:")
ydb_r_n = play_sin(1)
print("Rechtes Ohr mit verdeckung:")
ydb_l_n = play_sin(2)

plt.figure()
plt.plot(f, ydb_l, label='Linkes Ohr')
plt.plot(f, ydb_r, label='Rechtes Ohr')
plt.plot(f, ydb_l_n, label='Linkes Ohr mit Verdeckung')
plt.plot(f, ydb_r_n, label='Rechtes Ohr mit Verdeckung')
plt.xlim(20, 20000)  # Set x-axis
plt.ylim(0, 110)    # Set y-axis
plt.xscale('log')
plt.legend()
plt.title('Hörschwelle relativ zu 1kHz')
plt.xlabel('Frequenz (Hz)')
plt.ylabel('Hörschwelle (dB)')
plt.grid()
plt.show()

