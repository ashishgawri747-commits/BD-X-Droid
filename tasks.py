import subprocess
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import time
import threading
noise_process = subprocess.Popen(
     ["aplay", "-q", "--loop=0", "~/Music/back.wav"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

keepalive = subprocess.Popen(
   ["aplay", "-q","--loop=0","~/home/raspberry/silence.wav"])
engine = pyttsx3.init()
engine.setProperty('rate', 175)



class VoiceAssistant:
    def __init__(self):
        self.wake = ["friday", "underscore"]
        self.listening = True
        self.active = False
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=0)

        # Adjust energy threshold for better wake word detection
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

        with self.mic as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready to listen!")

    def say(self, t):
        if t: 
             print(f"Assistant: {t}")  
	     engine.say(t)
	     engine.runAndWait()

    def listen(self):
        try:
            with self.mic as source:
                print("Listening for command...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                try:
                    query = self.recognizer.recognize_google(audio, language="en-in")
                    print(f"User said: {query}")
                    return query.lower()
                except sr.UnknownValueError:
                    return None
                except sr.RequestError as e:
                    self.say("I think the mic might be glitching")
                    return None
        except sr.WaitTimeoutError:
            return None

    def listen_wake(self):
        print("Listening for wake word...")
        while self.listening:
            try:
                with self.mic as source:
                    # Add timeout to prevent indefinite blocking
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=3)
                try:
                    query = self.recognizer.recognize_google(audio, language="en-in")
                    query_lower = query.lower()
                    print(f"Heard: {query}")

                    # Check for wake word
                    if any(wake in query_lower for wake in self.wake):
                        self.say("Yes boss?")
                        self.active = True
                        self.handle_commands()
                        self.active = False
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    print("Recognition service error")
                    time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(0.5)

    def handle_commands(self):
        u = self.listen()
        if u is None:
            self.say("I didn't catch that")
            return

        try:
            if "open" in u:
                self.openinsites(u)
            elif "nothing" in u:
                self.say("Okay")
            elif "hi" in u or "hello" in u:
                self.say("Wassup mate")
            elif "time" in u:
                current_time = datetime.datetime.now().strftime("%H %M %S")
                self.say(f"Sir, the time is {current_time}")
            else:
                self.say("I'm not sure what you want me to do")
        except AttributeError:
            self.say("Sorry, something went wrong")

    def openinsites(self, m):
        # Define sites
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"]
        ]

        opera_path = r"C:\Users\Simran Gawri\AppData\Local\Programs\Opera GX\opera.exe"

        # Check websites
        for site in sites:
            if f"open {site[0]}" in m:
                self.say(f"Opening {site[0]}")
                try:
                    subprocess.Popen([opera_path, site[1]])
                    return
                except (subprocess.SubprocessError, FileNotFoundError):
                    print(f"Error opening {site[0]}")

        # Define apps
        apps = [
            ["notepad", "notepad.exe"],
            ["calculator", "calc.exe"],
            ["discord",
             "C:\\Users\\Simran Gawri\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc\\Discord.lnk"],
            ["spotify",
             "C:\\Users\\Simran Gawri\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Spotify.lnk"],
            ["photoshop", "photoshop.exe"],
            ["opera",
             "C:\\Users\\Simran Gawri\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Opera GX Browser.lnk"]
        ]

        # Check apps
        for app in apps:
            if f"open {app[0]}" in m:
                self.say(f"Opening {app[0]}")
                try:
                    os.startfile(app[1])
                    return
                except Exception as e:
                    print(f"Error opening {app[0]}: {e}")
                    self.say(f"Sorry, couldn't open {app[0]}")
                return

        # If nothing matched
        self.say("I couldn't find what you want to open")


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.listen_wake()
