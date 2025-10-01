import psutil
import asyncio
import platform
import os
import logging
from plyer import notification
from stt import speak

# --- SETTINGS ---
CHECK_INTERVAL = 60   # seconds
USE_VOICE = True      # Set False if you don’t want continuous speaking
SOUND_BACKEND = "pygame"   # choose: "pygame" or "simpleaudio"
SOUND_FILE = "alert.mp3"   # use .mp3 for pygame

# --- LOGGING ---
logging.basicConfig(
    filename="battery_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- SOUND FUNCTIONS ---
def play_sound():
    try:
        if SOUND_BACKEND == "pygame":
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(SOUND_FILE)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        else:
            logging.error(f"Unknown sound backend: {SOUND_BACKEND}")

    except Exception as e:
        logging.error(f"Error playing sound: {e}")


# --- SHUTDOWN FUNCTION ---
def shutdown():
    system = platform.system()
    match system:
        case "Windows":
            os.system("shutdown /s /t 1")
        case "Linux" | "Darwin":
            os.system("shutdown now")
        case _:
            logging.warning("Shutdown not supported on this OS.")


# --- BATTERY MONITOR ---
async def battery_alert():
    try:
        while True:
            battery = psutil.sensors_battery()
            if battery is None:
                logging.error("No battery detected.")
                return

            percent = int(battery.percent)
            plugged = battery.power_plugged

            # --- Full Battery ---
            if percent == 100 and plugged:
                msg = "Battery is 100%. Unplug the charger."
                if USE_VOICE: speak(msg)
                notification.notify(title="🔋 Battery Full", message=msg, timeout=5)
                play_sound()

            # --- Low Battery ---
            elif percent <= 20 and not plugged:
                msg = f"Battery is at {percent}%. Please plug in your charger."
                if USE_VOICE: speak(msg)
                notification.notify(title="⚠️ Low Battery", message=msg, timeout=5)
                play_sound()
            # --- Critical Battery Shutdown ---
            if percent <= 5 and not plugged:
                msg = "Battery critical! Shutting down."
                if USE_VOICE: speak(msg)
                notification.notify(title="💀 Critical Battery", message=msg, timeout=5)
                play_sound()
                await asyncio.sleep(1)
                shutdown()
                return

            # --- Log + Optional Voice ---
            log_msg = f"Battery: {percent}%, Charging: {plugged}"
            print(log_msg)
            logging.info(log_msg)
            if USE_VOICE:
                speak(f"Battery {percent} percent")
                speak("Charging" if plugged else "Not charging")

            await asyncio.sleep(CHECK_INTERVAL)

    except asyncio.CancelledError:
        logging.info("Battery monitor stopped.")
        if USE_VOICE: speak("Battery monitoring stopped. Goodbye!")
# --- MAIN ---
if __name__ == "__main__":
    try:
        asyncio.run(battery_alert())
    except KeyboardInterrupt:
        print("\nExiting battery monitor...")
