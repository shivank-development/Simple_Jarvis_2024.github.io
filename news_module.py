import requests
import random
from stt import speak
import time

API_KEY = "5484f80f87ac48488487687b0309e432"
BASE_URL = "https://newsapi.org/v2/top-headlines"
COUNTRY = "us"

VALID_CATEGORIES = {"business", "entertainment", "general", "health", "science", "sports", "technology"}

def get_news(category=None, count=100):
    try:
        params = {
            "country": COUNTRY,
            "apiKey": API_KEY
        }

        if category:
            cat = category.lower()
            if cat not in VALID_CATEGORIES:
                print(f"⚠️ Invalid category '{cat}'. Falling back to 'general'.")
                cat = "general"
            params["category"] = cat

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("status") != "ok" or not data.get("articles"):
            print("Full API Response for Debugging:\n", data)
            raise Exception("No news data available.")

        articles = data["articles"]
        random.shuffle(articles)

        selected = articles[:count]
        headlines = [article["title"] for article in selected]

        return headlines

    except Exception as e:
        error_msg = f"Error fetching news: {e}"
        print(error_msg)
        return []


# Example usage
headlines = get_news(category="technology")

if headlines:
    for i, headline in enumerate(headlines):
        print(headline)
        speak(f"Headline {i+1}: {headline}")
        
        # If not last headline → give hint for next one
        if i < len(headlines) - 1:
            speak("next news?")
            time.sleep(0.5)  # short pause before next
else:
    speak("Sorry, I could not fetch any news today.")
