import numpy as np
import sounddevice as sd
import threading
import keyboard

fs = 44100
current_y = 0.001
duration = 0.2
current_phase = 0  # in samples
f = 440

def callback(output, frames, time, status):
    global current_y, current_phase, f
    t = (np.arange(frames) + current_phase) / fs
    x = current_y * np.sin(2 * np.pi * f * t)
    output[:, 0] = x
    current_phase += frames
    if current_phase > fs * 10000:
        current_phase = current_phase % fs

def iterate_y(step):
    global current_y
    for y in range(0, 25532, step):
        current_y = y / 1000000
        sd.sleep(int(duration * 1000))
        print(current_y)


def iterate_f(resolution):
    global f, current_y
    for i in range(20, 450, resolution):
        f = i
        threading.Thread(target=iterate_y, args=(100,), daemon=True).start()
        sd.OutputStream(samplerate=fs, channels=1, callback=callback).start()
        print(f)
        if input('Press Enter to continue to the next frequency or type "exit" to stop: ') == 'exit':
            threading.Thread(target=iterate_y, args=(100,), daemon=True).join()
            break


iterate_f(10)
