import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import winsound
import scipy.io.wavfile as wav
import scipy.signal as sc

fs, rir4 = wav.read('RIR4 W25.wav')

mls = sc.max_len_seq(16)[0]

test = np.convolve(rir4, mls, mode='valid')

# sd.play(test, fs)
# sd.wait()

nfft = 2**int(np.ceil(np.log2(len(test))) + 1)
H = np.fft.rfft(test, n=nfft)
freqs = np.fft.rfftfreq(nfft, 1/fs)
H_db = 20 * np.log10(np.abs(H) + 1e-12)

plt.figure()
plt.semilogx(freqs, H_db)
plt.title('Amplitude frequency response (dB)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True, which='both', ls='--')
plt.show()


#def clarity(h, fs, t_ms):


#C50 = clarity(rir, fs, 50.0)
#C80 = clarity(rir, fs, 80.0)
