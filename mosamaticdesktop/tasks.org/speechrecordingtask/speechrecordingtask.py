import os
import shutil
import wave
import pyaudio

from mosamaticdesktop.tasks.task import Task


class SpeechRecordingTask(Task):
    def __init__(self) -> None:
        super(SpeechRecordingTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Records audio and saves it to .wav file',
        )
        self.addPathParameter(
            name='outputFileSetPath',
            labelText='Output File Set Path',
        )
        self.addTextParameter(
            name='outputFileSetName',
            labelText='Output File Set Name',
            optional=True,
        )
        self.addBooleanParameter(
            name='overwriteOutputFileSet',
            labelText='Overwrite Output File Set',
            defaultValue=True,
        )
        self._frames = []

    def execute(self) -> None:
        outputFileSetName = self.parameter('outputFileSetName').value()
        if not outputFileSetName:
            outputFileSetName = self.generateTimestampForFileSetName(name='modelOutput')
        outputFileSetPath = self.parameter('outputFileSetPath').value()
        outputFileSetPath = os.path.join(outputFileSetPath, outputFileSetName)
        overwriteOutputFileSet = self.parameter('overwriteOutputFileSet').value()
        if overwriteOutputFileSet:
            if os.path.isdir(outputFileSetPath):
                shutil.rmtree(outputFileSetPath)
        os.makedirs(outputFileSetPath, exist_ok=True)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        self.addInfo('Recording audio...')
        recording = True
        while recording:
            data = stream.read(1024)
            self._frames.append(data)
            if self.statusIsCanceled():
                self.addInfo('Stopping recording...')
                stream.stop_stream()
                stream.close()
                p.terminate()
                recording = False

        self.addInfo(f'Saving file recording.wav to: {outputFileSetPath}')
        wf = wave.open(os.path.join(outputFileSetPath, 'recording.wav'), 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self._frames))
        wf.close()        

        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
        self.addInfo('Finished')