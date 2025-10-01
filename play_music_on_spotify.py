import webbrowser
import pyautogui as ui
import time

def splay(text):
    webbrowser.open("http://open.spotify.com/")
    time.sleep(6)
    ui.hotkey("ctrl", "shift", "1")
    time.sleep(1)
    ui.write(text)
    time.sleep(2)
    ui.click(800, 500)
    ui.leftClick(800, 500)
    ui.leftClick(800, 500)

# ❌ REMOVE:
# x=input("Song_Name : ")
# splay(x)



"""
import webbrowser
import pyautogui as ui
import time

def splay(text):
    webbrowser.open("http://open.spotify.com/")
    time.sleep(6)
    ui.hotkey("ctrl", "shift", "1")
    time.sleep(1)
    ui.write(text)
    time.sleep(2)
    ui.click(800,500)
    ui.leftClick(800,500)
    ui.leftClick(800,500)


x=input("Song_Name : ")
splay(x)    
"""