"""
Title: Praxisaufgabe 3
Author: Robert Schleßmann
Kurs: Tontechnik 2
"""

import numpy as np
import librosa

tracks = ['./multitrack/01_SaxophoneCloseMic1.wav',
          './multitrack/02_SaxophoneCloseMic2.wav',
          './multitrack/03_SaxophoneFarMic1.wav',
          './multitrack/04_AcousticGtrCloseMics.wav',
          './multitrack/05_AcousticGtrFarMics.wav',
          './multitrack/06_AcousticGtrDI.wav']
energy = []
normalized_sig = []
signals = []

def calc_e(sig, sample_rate):
    return sum(sig**2)*(1/sample_rate)


def calc_corr(sig1, sig2):
    return (sum(sig1*sig2))/np.sqrt((sum(sig1**2))*(sum(sig2**2)))


def normalize(sigs):
    rms_ref = min(rms_vals)
    for z, r in zip(sigs, rms_ref):
        g = rms_ref / (r + 1e-12)
        normalized_sig.append(z*g)

for i in range(len(tracks)):
    x = librosa.load(tracks[i])[0]
    fs = librosa.load(tracks[i])[1]
    energy.append(calc_e(x, fs))
    rms_vals = np.sqrt(np.mean(x ** 2))
    signals.append(x)

energy_sum = sum(energy)
corr = calc_corr(librosa.load(tracks[0])[0], librosa.load(tracks[1])[0])
normalize(signals)
rms_sum = sum(normalized_sig)

print("Einzelenergien:", energy)
print("Gesamtenergie:", energy_sum)
print("Korrelationsgrad", corr)
print("Referenz RMS:")


