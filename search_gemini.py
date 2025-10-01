# search_gemini.py
import requests

API_KEY = "your api key"

def search_any_gemini(query: str) -> str:
    try:
        url = "https://api.gemini.ai/v1/query"  # Example endpoint
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {"prompt": query, "model": "gemini-mini", "max_tokens": 400}

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("answer") or result.get("text") or "No answer from Gemini."
    except Exception as e:
        print("Gemini failed:", e)
        return None
