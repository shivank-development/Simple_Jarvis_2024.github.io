import requests
import stt
import random
from Data.Dlg_online import internet_onstatus_message
from Data.Dlg_offline import internet_offstatus_message



def online_is(url="https://www.google.com", timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code >= 200 and response.status_code < 300
    except requests.ConnectionError:
        return False

def internet_status():
    if online_is():
        msg = internet_onstatus_message()
        stt.speak(msg)
        return "online"
    else:
        msg = internet_offstatus_message()
        stt.speak(msg)
        return "offline"

internet_status()
