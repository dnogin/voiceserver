import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import sys

# === Config ===
fs = 8000               # Sample rate (Hz)
freq = 440              # Frequency of sine wave
amplitude = 10000       # Amplitude of wave
duration = 0.01         # Duration of visible window in seconds (zoom level)
update_rate = 0.01     # Seconds between frames (~50 FPS)
scroll_speed = 1        # How many samples to move per frame

samples_visible = int(fs * duration)

# === Generate continuous sine wave ===
signal_length = 10 * fs
signal = (amplitude * np.sin(2 * np.pi * freq * np.arange(signal_length) / fs)).astype(np.int16)

# === PyQtGraph setup ===
app = QtWidgets.QApplication(sys.argv)
win = pg.GraphicsLayoutWidget(title="Live Waveform")
plot = win.addPlot()
plot.setYRange(-32768, 32767)
plot.setMouseEnabled(x=False, y=False)
plot.hideButtons()

curve = plot.plot(pen=pg.mkPen(color='b', width=1, cosmetic=True))  # crisp line
win.show()

# === Live update ===
i = 0
def update():
    global i
    start = i
    end = start + samples_visible
    if end > len(signal):
        chunk = np.concatenate((signal[start:], signal[:end - len(signal)]))
    else:
        chunk = signal[start:end]
    x = np.arange(len(chunk))
    curve.setData(x, chunk)
    i = (i + scroll_speed) % len(signal)

# === Run timer ===
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(int(update_rate * 1000))  # ms

# === Start app ===
sys.exit(app.exec())
