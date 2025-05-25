import curses
import time

import numpy as np
import numpy.typing as npt
import pyaudio
import wave

audio_obj = pyaudio.PyAudio()


def _record_audio(screen: curses.window) -> npt.NDArray[np.float32]:
    screen.nodelay(True)
    screen.clear()
    screen.addstr(
        'Press <spacebar> to start recording. Press <spacebar> again to stop recording.\n'
    )
    screen.refresh()

    recording = False
    audio_buffer: list[npt.NDArray[np.float32]] = []
    format = pyaudio.paInt16
    channels = 1
    rate = 48000
    chunk = 1024
    sample_width = 0

    while True:
        key = screen.getch()
        if key == ord(' '):
            recording = not recording
            if recording:
                screen.addstr('Recording started...\n')
                stream = audio_obj.open(format=format,
                                        channels=channels,
                                        rate=rate,
                                        input=True)
            else:
                screen.addstr('Recording stopped.\n')
                stream.stop_stream()
                stream.close()
                break
            screen.refresh()
        if recording:
            data = stream.read(chunk, exception_on_overflow=False)
            audio_buffer.append(data)
        time.sleep(0.01)

    converted_buffer = np.concatenate([np.frombuffer(a, dtype=np.int16, count=len(
        a)//2, offset=0).astype(np.float32, order='C') / 32768.0 for a in audio_buffer], axis=0)
    return converted_buffer


def record_audio():
    audio_data = curses.wrapper(_record_audio)
    return audio_data


def gen_empty_audio(seconds):
    return np.zeros(24000 * seconds, dtype=np.int16)


class AudioPlayer:
    def __enter__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 24000
        self.stream = audio_obj.open(format=self.format,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=False,
                                     output=True)
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.stream.stop_stream()
        self.stream.close()

    def add_audio(self, audio_data: npt.NDArray[np.int16]):
        audio_data_bytes = audio_data.tobytes()
        self.stream.write(audio_data_bytes)


if __name__ == '__main__':
    curses.wrapper(_record_audio)
