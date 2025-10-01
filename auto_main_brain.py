from web_open import open_web
from play_music_on_youtube import play as play_yt
from play_music_on_spotify import splay as play_spotify
from stt import speak, listen   # listen() will capture voice input
from threading import Thread


def auto_main_brain(text):
    text = text.lower()

    if any(word in text for word in ["open", "launch", "website", "start"]):
        open_web(text)


    elif "play on spotify" in text or "spotify" in text:
        query = text.replace("play on spotify", "").replace("spotify", "").strip()
        speak(f"Playing {query} on Spotify.")
        play_spotify(query)

    elif "battery" in text or "charging" in text:
        from battery import battery_alert
        Thread(target=battery_alert, daemon=True).start()
        speak("Battery monitoring started.")

    elif "exit" in text or "quit" in text:
        speak("Shutting down Jarvis.")
        exit()

    elif "weather" in text:
        from weather_module import get_weather
        speak(get_weather("Meerut"))

    elif "news" in text:
        from news_module import get_news
        speak(get_news())

    elif "check internet speed" in text or "net speed" in text or "check download speed" in text or "upload speed" in text:
        speak("This process may take a moment.")
        if "download" in text:
            from check_internet_speed import get_internet_speed
            get_internet_speed()
        else:
            from check_int import run_test
            run_test()

    # ---------------- SEARCH BLOCK WITH FALLBACK ----------------
    elif text.startswith(("search", "google", "find", "look for", 
                          "who is", "what is", "tell me about", 
                          "explain", "define", "give me information on")):
        query = text
        answer = None

        try:
            # 1. Try ChatGPT
            from Search import search_any  # your ChatGPT-based search
            answer = search_any(query)
        except Exception as e:
            print("ChatGPT failed:", e)

        if not answer:
            try:
                # 2. Try Gemini
                from search_gemini import search_any_gemini
                answer = search_any_gemini(query)
            except Exception as e:
                print("Gemini failed:", e)

        if not answer:
            try:
                # 3. Try Google AI
                from search_google import search_any_google
                answer = search_any_google(query)
            except Exception as e:
                print("Google AI failed:", e)

        if not answer:
            answer = "Sorry, I could not find an answer from ChatGPT, Gemini, or Google AI."
            speak(answer)

        speak(answer)
        print(f"Jarvis: {answer}")

    # ---------------- GREETING HANDLER ----------------
    elif text.startswith(("hey jarvis", "okay jarvis", "hi jarvis", "hello jarvis",
                          "hey chatgpt", "okay chatgpt", "hi chatgpt", "hello chatgpt")):
        speak("Yes, I am here. How can I help you?")
        query = text
        from Search import search_any
        answer = search_any(query)
        speak(answer)
        print(f"Jarvis: {answer}")

        # ---------------- CLOSE APP HANDLER ----------------
    elif "close" in text:
        app = text.replace("close", "").replace("app", "").strip()
        if app:
            from order_to_stop import close_app
            speak(f"Closing {app}")
            close_app(app)
        else:
            speak("Please tell me which app to close.")
     

    else:
        speak("Sorry, I didn't understand that.")


# Run only when executed directly
if __name__ == "__main__":
    from check_network import internet_status
    internet_status()
    speak("Jarvis is ready. Listening for your commands...")
    while True:
        user_input = listen(text="")  #
        print(f"User: {user_input}") # listen() function to capture voice input
        if user_input:
            auto_main_brain(user_input)
            speak("Listening for next command...")
