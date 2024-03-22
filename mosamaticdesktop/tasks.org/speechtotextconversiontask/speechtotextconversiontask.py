import os
import ssl
import shutil
import whisper

# Requires installation of "ffmpeg" on your local system

from mosamaticdesktop.tasks.task import Task


class SpeechToTextConversionTask(Task):
    def __init__(self) -> None:
        super(SpeechToTextConversionTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Loads audio file (MP3) and converts it to text using Coqui-TTS package',
        )
        self.addFilePathParameter(
            name='inputFilePath',
            labelText='Input File Path to WAV Audio File',
        )
        self.addOptionGroupParameter(
            name='modelName',
            labelText='Model Name',
            options=['base', 'medium', 'large'],
            defaultValue='large',
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

    def execute(self) -> None:
        # Hack: some CA certificate does not seem to be installed and giving errors when connecting to OpenAI
        ssl._create_default_https_context = ssl._create_unverified_context

        inputFilePath = self.parameter(name='inputFilePath').value()
        modelName = self.parameter(name='modelName').value()
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

        step = 0
        nrSteps = 2
        self.addInfo(f'Loading model {modelName}...')
        model = whisper.load_model(modelName)
        self.updateProgress(step=step, nrSteps=nrSteps)
        step += 1
        self.addInfo(f'Transcribing audio file {inputFilePath}...')
        modelOutput = model.transcribe(inputFilePath)
        self.updateProgress(step=step, nrSteps=nrSteps)
        step += 1

        self.addInfo(f'Building output fileset: {outputFileSetPath}')
        with open(os.path.join(outputFileSetPath, 'modelOutput.txt'), 'w') as f:
            f.write(modelOutput['text'])
        self.dataManager().createFileSet(fileSetPath=outputFileSetPath)
        # Add warning to it automatically shows up with the transcribed text
        self.updateProgress(step=step, nrSteps=nrSteps)
        self.addError(modelOutput['text'])