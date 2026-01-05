import os
from groq import Groq
import sounddevice as sd
from scipy.io import wavfile
from pathlib import Path
import subprocess

# Initialize Groq client
groq_client = Groq(api_key="")

# Audio settings for Google Voice HAT
DEVICE = 0
SAMPLE_RATE = 48000
CHANNELS = 2
DURATION = 5

speech = False
speecherror = False

def transcribe():
    full_transcript = ""
    print("Speak")
    try:
        print("listening")
        # Record audio
        audio = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int32',
            device=DEVICE,
            blocksize=1024
        )
        sd.wait()
        print("recognizing")
        
        # Save to temp file
        filepath = Path('/tmp/audio.wav')
        wavfile.write(filepath, SAMPLE_RATE, audio)
        
        # Transcribe with Groq
        with open(filepath, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(filepath.name, file.read()),
                model="whisper-large-v3-turbo",
                language="en",
                response_format="text"
            )
        
        full_transcript += transcription
        speech = True
        speecherror = False
        
    except Exception as e:
        print(f"Error: {e}")
        speech = False
        speecherror = True
        
    finally:
        return full_transcript

e = input("Press Enter to start: ")
if e in "Yy" or e == "":
    result = transcribe()
    print(f"You said: {result}")
