"""
import pyttsx3
engine = pyttsx3.init()
engine.say("Hello! This is a text to speech example.")
engine.runAndWait()

from gtts import gTTS
import os
tts = gTTS("Namaste! Welcome to your custom TTS app.", lang='en')
#tts=gTTS("नमस्ते! कैसे हो?", lang='hi')  # Hindi

tts.save("output.mp3")
os.system("start output.mp3")  # Windows: play audio

"""
import speech_recognition as sr
import pyttsx3
import time
from threading import Thread


def speak(text):
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS Error:", e)

# Callback for when speech is detected
def _callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        # Send recognized text to Jarvis brain
        from auto_main_brain import auto_main_brain
        auto_main_brain(text)
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError:
        print("❌ Could not request results; check your internet connection.")

# Continuous listening function
def listen(text):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Adjust for ambient noise once
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Jarvis is ready. Listening continuously...")

    # Start background listening
    stop_listening = recognizer.listen_in_background(mic, _callback)

    # Keep main thread alive without blocking
    try:
        while True:
            time.sleep(0.1)  # <-- small sleep prevents 100% CPU usage
    except KeyboardInterrupt:
        stop_listening(wait_for_stop=False)
        print("Stopped listening.")
