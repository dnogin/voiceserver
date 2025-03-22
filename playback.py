import sounddevice as sd
import numpy as np
from queue import Queue, Empty

class AudioPlayer:
    def __init__(self, rate=8000):
        self.rate = rate
        self.buffer = Queue()
        self.stream = sd.OutputStream(
            samplerate=self.rate,
            channels=1,
            dtype='int16',
            callback=self.callback,
            blocksize=1024
        )
        self.stream.start()

    def play(self, data: np.ndarray):
        # Push audio to the buffer
        self.buffer.put(data)

    def callback(self, outdata, frames, time, status):
        try:
            chunk = self.buffer.get_nowait()
        except Empty:
            # Fill with silence if nothing in buffer
            outdata[:] = np.zeros((frames, 1), dtype='int16')
        else:
            # Reshape and write to output buffer
            out = chunk[:frames]
            if out.ndim == 1:
                out = out.reshape(-1, 1)
            if len(out) < frames:
                pad = np.zeros((frames - len(out), 1), dtype='int16')
                out = np.vstack([out, pad])
            outdata[:] = out
