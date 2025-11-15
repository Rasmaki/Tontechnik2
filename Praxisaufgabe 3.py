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


def calc_e(sig, sample_rate):
    return sum(sig**2)*(1/sample_rate)


def calc_corr(sig1, sig2):
    return (sum(sig1*sig2))/np.sqrt((sum(sig1**2))*(sum(sig2**2)))


for i in range(len(tracks)):
    x = librosa.load(tracks[i])[0]
    fs = librosa.load(tracks[i])[1]
    energy.append(calc_e(x, fs))

energy_sum = sum(energy)
corr = calc_corr(librosa.load(tracks[0])[0], librosa.load(tracks[1])[0])
print("Einzelenergien:", energy)
print("Gesamtenergie:", energy_sum)
print("Korrelationsgrad", corr)
