#!/usr/bin/env python3.8
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import re
import pkg_resources
 

resource_path = pkg_resources.resource_filename(__name__, '/vosk-model-small-cn-0.22')


class MicRecognizer:
    def __init__(self):
        self._q = queue.Queue()
        self.device_info = sd.query_devices(None, "input")
        self._samplerate = int(self.device_info["default_samplerate"])
        self._rec = KaldiRecognizer(Model(resource_path), self._samplerate)
        self.rec_result = queue.Queue()
        self.work = True

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        self._q.put(bytes(indata))

    def start(self):
        self.work = True
        with sd.RawInputStream(samplerate=self._samplerate, blocksize=1024*8, 
                               dtype="int16", channels=1, callback=self._callback):
            print('<-Mic Recognizer Working...->')

            try:
                while self.work:
                    data = self._q.get()
                    if self._rec.AcceptWaveform(data):
                        text = eval(self._rec.Result())["text"]
                        text = re.sub(r'\s+', '', text)
                        if text:
                            self.rec_result.put(text)
                            # print(text)
            except KeyboardInterrupt:
                self.end()

    def end(self):
        self.work = False
        print('<-Mic Recognizer END->')


if __name__ == '__main__':
    recognizer = MicRecognizer()
    recognizer.start()
