import pyaudio
import wave
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import librosa
import torch, gc

print('load model and tokenizer')

device = "cuda:0" if torch.cuda.is_available() else "cpu"
# device = 'cpu'
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
model = model.to(device)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=1)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print('* saved recording')

print('load audio')
audio, rate = librosa.load("output.wav", sr = 16000)

print('tokenize')
input_values = tokenizer(audio, return_tensors = "pt").input_values.to(device)

print('prediction')
logits = model(input_values).logits

print('take argmax and decode')
prediction = torch.argmax(logits, dim = -1)
transcription = tokenizer.batch_decode(prediction)[0]

print(transcription)

gc.collect()
torch.cuda.empty_cache()