# search_google.py
import requests

API_KEY = "your api key"
CX = "YOUR_GOOGLE_CSE_ID"  # for Google Custom Search

def search_any_google(query: str) -> str:
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": API_KEY,
            "cx": CX,
            "q": query
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])
        if not items:
            return "No results from Google AI."
        top_result = items[0]
        return f"{top_result.get('title')}: {top_result.get('snippet')}"
    except Exception as e:
        print("Google AI failed:", e)
        return None
