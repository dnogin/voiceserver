import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import sys
import threading
from collections import deque

class WaveformDisplay:
    def __init__(self, rate=8000, max_seconds=1):
        self.rate = rate
        self.samples_visible = int(rate * max_seconds)
        self.buffer = deque(maxlen=self.samples_visible)
        self.app = None
        self.timer = None
        self.i = 0

        # Setup GUI in main thread
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(title="Live Waveform")
        self.plot = self.win.addPlot()
        self.plot.setYRange(-32768, 32767)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.hideButtons()

        self.curve = self.plot.plot(pen=pg.mkPen(color='b', width=1, cosmetic=True))

        self.x = np.arange(self.samples_visible)
        self.y = np.zeros(self.samples_visible, dtype=np.int16)

    def start(self):
        self.win.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update_plot)
        self.timer.start(50)

    def update(self, data):
        self.buffer.extend(data)

    def _run(self):
        self.win.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update_plot)
        self.timer.start(50)  # 20 FPS

        sys.exit(self.app.exec())

    def _update_plot(self):
        if len(self.buffer) == 0:
            return
        data = list(self.buffer)
        y = np.array(data, dtype=np.int16)
        x = np.arange(len(y))
        self.curve.setData(x, y)
