import config
import pvporcupine
import vosk
from pvrecorder import PvRecorder

porcupine = pvporcupine.create(
    access_key=config.PICOVOICE_TOKEN, keywords=["jarvis"], sensitivities=[1]
)

model = vosk.Model("../vosk_model")
samplerate = 16000
kaldi_rec = vosk.KaldiRecognizer(model, samplerate)
recorder = PvRecorder(
    device_index=config.MICROPHONE_INDEX, frame_length=porcupine.frame_length
)
