import webbrowser
import os
import pyautogui
import stt
from tkinter import Tk, messagebox

# Dummy speak function for testing (replace with actual TTS later)
def speak(text):
    print("SPEAK:", text)
    stt.speak(text)

websites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "github": "https://www.github.com",
    "instagram": "https://www.instagram.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chat.openai.com",
    "reddit": "https://www.reddit.com",
    "linkedin": "https://www.linkedin.com",
    "twitter": "https://www.twitter.com",
    "stackoverflow": "https://stackoverflow.com",
    "spotify": "https://open.spotify.com"
}

# Words to strip from user input
command_keywords = ["open", "start", "run", "launch", "play", "app", "application"]
exit_keywords = ["close", "exit", "stop", "quit"]

def open_web(text):
    original = text
    text = text.lower().strip()

    # 🚪 Check for exit command
    for exit_word in exit_keywords:
        if exit_word in text:
            speak("Closing assistant.")
            exit()

    # Remove extra keywords like "open", "start"
    for word in command_keywords:
        if word in text:
            text = text.replace(word, "").strip()

    # 🌐 1️⃣ Website match
    for name in websites:
        if name in text:
            speak(f"Opening {name} website.")
            webbrowser.open(websites[name])
            return

    # 🌐 2️⃣ URL-like input
    if "." in text:
        if not text.startswith("http"):
            text = "https://" + text
        speak(f"Opening {text}")
        webbrowser.open(text)
        return

    # 🖥️ 3️⃣ Try os.system
    try:
        print(f"Trying os.system to open: {text}")
        exit_code = os.system(f'start "" "{text}"')
        if exit_code == 0:
            speak(f"Opening {text}")
            return
        else:
            raise Exception("System couldn't find it")
    except Exception as e:
        print("os.system failed:", e)

    # ⌨️ 4️⃣ Fallback to pyautogui
    try:
        print(f"Fallback to pyautogui: {text}")
        speak(f"Trying to open {text} using search...")
        pyautogui.press('win')
        pyautogui.write(text, interval=0.3)
        pyautogui.press('enter')
    except Exception as e:
        print("pyautogui failed:", e)
        try:
            speak("Sorry, I couldn't open it.")
            Tk().withdraw()
            messagebox.showerror("App Not Found", f"Could not open {text}")
        except:
            pass


# 👂 Main loop
"""while True:
    x = input("data: ")
    open_web(x)"""
