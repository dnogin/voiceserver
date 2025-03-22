import sounddevice as sd
import numpy as np
from queue import Queue, Empty

class AudioPlayer:
    def __init__(self, rate=8000):
        self.rate = rate
        self.buffer = Queue()
        self.cache = np.zeros((0,), dtype='int16')  # Holds leftover audio
        self.stream = sd.OutputStream(
            samplerate=self.rate,
            channels=1,
            dtype='int16',
            callback=self.callback,
            blocksize=1024
        )
        self.stream.start()

    def play(self, data: np.ndarray):
        self.buffer.put(data)

    def callback(self, outdata, frames, time, status):
        samples_needed = frames

        # Fill up cache if needed
        while len(self.cache) < samples_needed:
            try:
                new_chunk = self.buffer.get_nowait()
                self.cache = np.concatenate((self.cache, new_chunk))
            except Empty:
                break

        if len(self.cache) >= samples_needed:
            out = self.cache[:samples_needed]
            self.cache = self.cache[samples_needed:]
        else:
            # Not enough data, pad with silence
            out = np.zeros((samples_needed,), dtype='int16')

        outdata[:] = out.reshape(-1, 1)
