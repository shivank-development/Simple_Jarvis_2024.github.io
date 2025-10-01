import os
import pygame
from winotify import Notification, audio

# Paths
BASE_DIR = os.getcwd()
ICON_PATH = os.path.join(BASE_DIR, "image.png")
ALERT_SOUND = os.path.join(BASE_DIR, "alert.mp3")

def play_alert(sound_file: str):
    """Play custom alert sound using pygame"""
    if os.path.exists(sound_file):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Wait until sound finishes
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"[ERROR] Unable to play sound: {e}")
    else:
        print("[WARNING] Alert sound file not found!")

def show_notification(title: str, message: str, link: str = None):
    """Show Windows toast notification with optional link"""
    toast = Notification(
        app_id="OPEN SKILL",
        title=title,
        msg=message,
        duration="long",
        icon=ICON_PATH if os.path.exists(ICON_PATH) else None
    )

    # Keep default Windows notification sound
    toast.set_audio(audio.Default, loop=False)

    # Add action button if link is provided
    if link:
        toast.add_actions(label="Open Link", launch=link)

    toast.show()

if __name__ == "__main__":
    # Play custom alert first
    play_alert(ALERT_SOUND)

    # Show toast notification
    show_notification("Alert ⚠️", "Attention Required!", "https://www.google.com")
