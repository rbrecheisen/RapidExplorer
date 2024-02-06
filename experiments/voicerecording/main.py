import sys
import wave
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
# from pydub import AudioSegment
import pyaudio
import threading

class VoiceRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_recording = False
        self.frames = []

    def initUI(self):
        self.setWindowTitle("Voice Recorder")
        layout = QVBoxLayout()
        
        self.start_button = QPushButton("Start Recording")
        self.start_button.setEnabled(True)
        self.start_button.clicked.connect(self.startRecording)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stopRecording)
        layout.addWidget(self.stop_button)
        
        self.save_button = QPushButton("Save Recording")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.saveRecording)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)

    def startRecording(self):
        self.is_recording = True
        self.frames = []        
        self.thread = threading.Thread(target=self.record)
        self.thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.save_button.setEnabled(False)

    def stopRecording(self):
        self.is_recording = False
        self.thread.join()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.save_button.setEnabled(True)

    def record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        
        while self.is_recording:
            data = stream.read(1024)
            self.frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()

    def saveRecording(self):
        wf = wave.open('recording.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()        
        # sound = AudioSegment.from_wav('recording.wav')
        # sound.export('recording.mp3', format='mp3')
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    recorder = VoiceRecorder()
    recorder.show()
    sys.exit(app.exec())
