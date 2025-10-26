"""
created: 15-10-2025
Version: 1.0
Beschreibung: Dieses Programm führt einen einfachen Hörtest durch, bei dem Sinustöne verschiedener Frequenzen
und Pegel abgespielt werden. Der Benutzer gibt an, ob er den Ton gehört hat, und die Hörschwelle wird für jedes Ohr
ermittelt. Zusätzlich wird ein Rauschsignal abgespielt, um den Verdeckungseffekt zu demonstrieren.
@author: Robert Schleßmann
"""

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import threading

fs = sd.query_devices(sd.default.device, 'output')['default_samplerate'] # Abtastrate ermitteln
dur = 1 # Dauer in Sekunden
ydb = np.arange(40, 105, 5) # Pegel in dB, von 40 bis 100 dB in 5 dB Schritten
y = (10**(ydb/10))/10000000000 # Umrechnung in lineare Amplitude
t = np.arange(dur * fs) / fs # Zeitvektor
f = [125, 250, 500, 1000, 2000, 4000, 8000]  # Frequenzen


def play_sin(ch):
    """Spielt eine Sinuswelle auf dem angegebenen Kanal ab und überprüft das Hörvermögen des Nutzers."""
    global y, f, t, ydb, fs
    ydb_temp = np.array([]) # Zurücksetzen des Pegel-Arrays auf einen leeren Zustand
    for j in range(len(f)):
        for i in range(len(y)):
            x =  y[i] * np.sin(2 * np.pi * f[j] * t) # Sinuswelle generieren
            sd.play(x, fs, mapping=[ch]) # Sinuswelle auf dem angegebenen Kanal abspielen
            sd.wait()
            usr_input = input("Haben Sie den Ton gehört? Y/N...")
            if usr_input == 'y': # Eingabe von 'y' bedeutet, dass der Ton gehört wurde
                print("Deine Hörschwelle bei {1} Hz ist {0} dB".format(ydb[i], f[j]))
                ydb_temp = np.append(ydb_temp, ydb[i]) # Momentanen Pegel zum Array hinzufügen
                break
    ydb_temp = ydb_temp - ydb_temp[3] # Normalisierung auf 1kHz
    return ydb_temp


def play_noise(rms=0.0001):
    """Spielt Rauschsignal ab, um den Verdeckungseffekt darzustellen."""
    global t

    event = threading.Event() # Initialisieren eines Events zum Stoppen des Rauschens

    def callback(outdata, frames, time, status):
        """Stream-Callback-Funktion zum Generieren von Rauschen."""
        if status:
            pass
        noise = np.random.normal(0, 1.0, size=(frames, 1)).astype(np.float32) # Weißes Rauschen generieren
        cur_rms = np.sqrt(np.mean(noise**2)) # Aktuellen RMS-Wert berechnen
        noise *= (rms/cur_rms) # Rauschen auf gewünschten RMS-Wert skalieren
        outdata[:] = noise # Rauschsignal zur Stream-Ausgabe zuweisen

    noise_stream = sd.OutputStream(channels=1, callback=callback, samplerate=fs) # Rausch-Stream initialisieren und
    noise_stream.start() # Rausch-Stream starten

    try:
        event.wait() # Warten, bis das Event gesetzt wird
    finally:
        noise_stream.stop() # Rausch-Stream stoppen
        noise_stream.close()

    return event


# Hauptprogramm zur Durchführung des Hörtests
print("Linkes Ohr:")
ydb_l = play_sin(1) # Hörtest für linkes Ohr (Kanal 1)
print("Rechtes Ohr:")
ydb_r = play_sin(2) # Hörtest für rechtes Ohr (Kanal 2)
threading.Thread(target=play_noise, daemon=True).start() # Rauschsignal in einem separaten Thread starten
print("Linkes Ohr mit verdeckung:")
ydb_r_n = play_sin(1) # Hörtest für linkes Ohr mit Rauschverdeckung (Kanal 1)
print("Rechtes Ohr mit verdeckung:")
ydb_l_n = play_sin(2) # Hörtest für rechtes Ohr mit Rauschverdeckung (Kanal 2)


# Plotten der Ergebnisse
fig, ax = plt.subplots()
ax.set_xscale('log')
ax.set_xlim(100, 10000)  # Set x-axis
ax.set_ylim(-40, 40)    # Set y-axis
ax.set_title('Hörschwelle relativ zu 1kHz')
ax.set_xlabel('Frequenz (Hz)')
ax.set_ylabel('Hörschwelle (dB)')


plt.plot(f, ydb_l, label='Linkes Ohr', marker='o')
plt.plot(f, ydb_r, label='Rechtes Ohr', marker='o')
plt.plot(f, ydb_l_n, label='Linkes Ohr mit Verdeckung', marker='o')
plt.plot(f, ydb_r_n, label='Rechtes Ohr mit Verdeckung', marker='o')

ax.xaxis.set_major_formatter(ScalarFormatter())
ax.minorticks_off()
ax.set_xticks(f)

plt.legend()
plt.grid()
plt.show()
