import speech_recognition as sr
recognizer=sr.Recognizer()
recognizer.energy_threshold=500
recognizer.dynamic_energy_threshold=True
mic=sr.Microphone(device_index=0, sample_rate=48000, chunk_size=1024)
speech=False
speecherror=False

def transcribe():
        full_transcript=""
        print("Speak")
        try:
                with mic as source:
                      recognizer.adjust_for_ambient_noise(source, duration=1)
                print("speak")
                with mic as source:
                     print("listening")
                     audio=recognizer.listen(source, timeout=5, phrase_time_limit=15)
                     print("recognizin")
                     text=recognizer.recognize_google(audio)
                     full_transcript+="" + text
                speech=True
                speecherror=False
        except sr.WaitTimeoutError:
                print("no speech")
                speech=False
                speecherror=True
        except sr.UnknownValueError:
                print("value error")
                speech=False
                speecherror=True
        finally:
                return full_transcript
e=input("enter")
if e in "Yy":
        result=transcribe()
        print(result)
