#!/usr/bin/env python3.8
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import re
import pkg_resources
from time import sleep
 

resource_path = pkg_resources.resource_filename(__name__, '/vosk-model-small-cn-0.22')


class MicRecognizer:
    def __init__(self):
        self._q = queue.Queue()
        self.device_info = sd.query_devices(None, "input")
        self._samplerate = int(self.device_info["default_samplerate"])
        self._rec = KaldiRecognizer(Model(resource_path), self._samplerate)
        self.rec_result = queue.Queue()
        self.work = True
        self.listen = True

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        self._q.put(bytes(indata))

    def start(self):
        self.work = True
        self.open_ear()
        with sd.RawInputStream(samplerate=self._samplerate, blocksize=1024*8, 
                               dtype="int16", channels=1, callback=self._callback):
            print('<-Mic Recognizer Working...->')

            try:
                while self.work:
                    data = self._q.get()
                    if not self.listen:
                        sleep(0.001)
                        continue
                    if self._rec.AcceptWaveform(data):
                        text = eval(self._rec.Result())["text"]
                        # print('1'+text)
                        text = re.sub(r'\s+', '', text)
                        # print('2'+text)
                        if len(text)>2:
                            text.replace('防线','房间')
                            self.rec_result.put(text)
                            # print(text)
            except KeyboardInterrupt:
                self.end()

    def close_ear(self):
        self.listen = False

    def open_ear(self):
        self.listen = True
        while (not self.rec_result.empty()):
            sleep(0.001)
            self.rec_result.get()

    def end(self):
        self.work = False
        print('<-Mic Recognizer END->')


if __name__ == '__main__':
    recognizer = MicRecognizer()
    recognizer.start()
