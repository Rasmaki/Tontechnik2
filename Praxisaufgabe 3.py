import numpy as np
import librosa

tracks = [
    'multitrack/01_SaxophoneCloseMic1.wav',
    'multitrack/02_SaxophoneCloseMic2.wav',
    'multitrack/03_SaxophoneFarMic1.wav',
    'multitrack/04_AcousticGtrCloseMics.wav',
    'multitrack/05_AcousticGtrFarMics.wav',
    'multitrack/06_AcousticGtrDI.wav' #korrekte Pfade nötig
]
energy = []
signals = []

def calc_e(sig, sample_rate):
    return np.sum(sig**2) * (1/sample_rate)

def calc_corr(sig1, sig2):
    numerator = np.sum(sig1 * sig2)
    denominator = np.sqrt(np.sum(sig1**2) * np.sum(sig2**2))
    return numerator / denominator

def calc_rms(sig):
    squared_signal = sig**2 #Quadrieren der Abtastwerte (x[n]^2)
    squared_sum = np.sum(squared_signal)
    N = len(sig)
    mean_square = squared_sum / N #Teilen durch Anzahl Abtastwerte N (mittlere Leistungsgröße)
    RMS = np.sqrt(mean_square)

    return RMS

for i in range(len(tracks)):
    x, fs = librosa.load(tracks[i], sr=None)
    energy.append(calc_e(x, fs)) #Energie speichern
    signals.append(x) #signals Array

#Summensignal initialisieren
sum_signal = np.zeros_like(signals[0])
leveled_signals = []
gain_list_dB = []
sample_rate = fs #Sample Rate speichern
n = len(signals) #Anzahl der Tracks
L_max_dBFS = -6.0 #Summe Zielpegel, -6.0dBFS als Obergrenze
headroom_dB = 10 * np.log10(n) #Berechnung Pegelgewinn (Formel_: deltaL = 10*log10(n)
L_target_dBFS = L_max_dBFS - headroom_dB #Zielpegel je Einzeltrack

for sig in signals:
    rms_i = calc_rms(sig) #Berechnung RMS
    current_level_dBFS = 20 * np.log10(rms_i) #Pegel in dBFS
    gain_dB = L_target_dBFS - current_level_dBFS #Berechnung benötigten Gains in dB
    gain_linear = 10**(gain_dB / 20) #Gain umrechnen (dB in Linear)
    sig_leveled = sig * gain_linear #Pegeln vom Signal (Multiplizieren des ursprünglichen Signals mit linearem
    sum_signal = sum_signal + sig_leveled #Summensignal (Addieren des Ursprünglichem Signals und dem linearen
    leveled_signals.append(sig_leveled) #Speichern des gepegelten Einzeltracks in die Liste leveled_signals
    gain_list_dB.append(gain_dB)

rms_sum = calc_rms(sum_signal) #RMS vom Summensignal
final_sum_level_dBFS = 20 * np.log10(rms_sum) #Pegel vom Summensignal

print("Korrelationsgrad:", calc_corr(librosa.load(tracks[0])[0], librosa.load(tracks[1])[0]))
print(f"Schätzung für das technische Pegeln")
print(f"Anzahl der Tracks: {n}")
print(f"Geschätzter Pegelgewinn (Summe, deltaL): {headroom_dB:.2f}dB")
print(f"Ziel-Summenpegel: {L_max_dBFS:.2f}")
print(f"Zielpegel pro Track: {L_target_dBFS:.2f}dBFS")
print(f"\n--- Überprüfung: Technisches Pegeln ---")
print(f"Erwarteter Summenpegel (L_max): {L_max_dBFS:.2f} dBFS")
print(f"Erreichter Summenpegel: {final_sum_level_dBFS:.2f} dBFS")