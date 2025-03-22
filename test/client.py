import asyncio
import wave
import websockets

SAMPLE_RATE = 8000
CHUNK_SIZE = 1024  # same as server expects
WAV_FILE = "test.wav"

async def stream_audio():
    async with websockets.connect("ws://localhost:8765") as websocket:
        print("Connected to server")
        with wave.open(WAV_FILE, 'rb') as wf:
            assert wf.getnchannels() == 1
            assert wf.getframerate() == SAMPLE_RATE
            assert wf.getsampwidth() == 2  # 16-bit PCM

            while True:
                data = wf.readframes(CHUNK_SIZE)
                if not data:
                    break
                await websocket.send(data)
                await asyncio.sleep(CHUNK_SIZE / SAMPLE_RATE)  # sync with real time

if __name__ == "__main__":
    asyncio.run(stream_audio())
