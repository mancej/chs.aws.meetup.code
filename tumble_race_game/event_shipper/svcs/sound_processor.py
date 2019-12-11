import pyaudio
import wave
import logging
import boto3
import os

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class SoundProcessor:
    CHUNK = 1024  # Record in chunks of 1024 samples
    FORMAT = pyaudio.paInt16  # 16 bits per sample
    CHANNELS = 1
    FS = 44100  # Record at 44100 samples per second
    SECONDS = 3
    FILENAME = "output.wav"

    def __init__(self):
        self._pyaudio = pyaudio.PyAudio()
        self._s3 = boto3.resource('s3')

    def record(self, duration: int, file_name: str):
        stream = self._pyaudio.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.FS,
                        frames_per_buffer=self.CHUNK,
                        input=True)

        log.info('########################################')
        log.info('######## Recording STARTED #############')
        log.info('########################################')


        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for i in range(0, int(self.FS / self.CHUNK * duration)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        stream.close()

        log.info('########################################')
        log.info('######## Recording COMPLETE #############')
        log.info('########################################')

        file_name = f'{file_name}.wav'
        file_path = f'/tmp/{file_name}'
        # Save the recorded data as a WAV file
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self._pyaudio.get_sample_size(self.FORMAT))
        wf.setframerate(self.FS)
        wf.writeframes(b''.join(frames))
        wf.close()

        log.info("Copying file!")
        s3_obj = self._s3.Object('saj-prod-devops-ui', f'audio-uploads/{file_name}')
        s3_obj.upload_file(file_path)
        log.info("File copied!")

        # os.remove(file_path)



