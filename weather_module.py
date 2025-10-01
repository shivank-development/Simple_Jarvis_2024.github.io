import requests
from stt import speak

def get_weather(city):
    api_key = "629fe03d775e8764ce019058e2163db7"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    res = requests.get(url).json()

    if res.get("main"):
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        weather_report = f"The temperature in {city} is {temp}°C with {desc}."
        return weather_report
    else:
        return f"Sorry, I could not fetch the weather for {city}."

def ask_weather():
    speak("Please type the city name.")
    city = input("Enter your city: ")   # manual input for now
    if not city:
        speak("No city entered. Please try again.")
        return
    
    report = get_weather(city)
    print(report)   # debug/log
    speak(report)

# Example: call this when user asks Jarvis about weather
ask_weather()
