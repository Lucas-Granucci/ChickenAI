import pyttsx3
import threading

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 220)
        self.speaking = False

    def say(self, text: str) -> None:
        self.speaking = True
        def run_speech():
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
        
        thread = threading.Thread(target=run_speech)
        thread.start()

    def stop(self) -> None:
        if self.speaking:
            self.engine.stop()
            self.speaking = False