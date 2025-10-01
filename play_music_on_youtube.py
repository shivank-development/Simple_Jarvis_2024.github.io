import webbrowser
import psutil

youtube_open = False

def play(text: str) -> str:
    """Play or stop YouTube based on the user's command."""
    global youtube_open
    text = text.lower().strip()

    # Stop YouTube
    if "stop" in text and "youtube" in text:
        closed = False
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                pname = proc.info['name'].lower() if proc.info['name'] else ""
                if any(browser in pname for browser in ["chrome", "msedge", "firefox"]):
                    proc.kill()
                    closed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        youtube_open = False
        return "✅ Closed YouTube browser." if closed else "⚠️ No YouTube browser found."

    # Play something on YouTube
    elif "youtube" in text and not youtube_open:
        query = text.replace("youtube", "").strip().replace(" ", "+")
        if query == "":
            return "⚠️ Please tell me what to play on YouTube."
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        youtube_open = True
        return f"🎵 Opening YouTube for '{query}'..."

    # Already open
    elif youtube_open:
        return "▶️ YouTube is already open."

    # Fallback
    else:
        return "⚠️ I didn't understand your YouTube command."


# ===========================
# Jarvis main loop
# ===========================
"""if __name__ == "__main__":
    print("🤖 Jarvis is ready! (type your command, 'exit' to quit)\n")
    while True:
        command = input("You: ")

        if command.lower() == "exit":
            print("👋 Goodbye, master!")
            break

        response = play(command)
        print("Jarvis:", response)"""
