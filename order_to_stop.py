# order_to_stop.py
import psutil
import subprocess

def close_app(app_name):
    """
    Closes an application by its process name (Windows safe).
    Example: "chrome", "notepad", "code"
    """
    found = False
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            pname = proc.info['name'].lower() if proc.info['name'] else ""
            if app_name.lower() in pname:
                proc.terminate()   # try safe terminate
                print(f"Closed {pname} (PID: {proc.info['pid']})")
                found = True
        except (psutil.NoSuchProcess, psutil.ZombieProcess):
            pass
        except psutil.AccessDenied:
            print(f"Access denied while trying to close {proc.info['name']}")

    if not found:
        print(f"No running process found with name containing '{app_name}'")
        # Try force close with taskkill
        try:
            subprocess.run(f"taskkill /f /im {app_name}.exe", shell=True, capture_output=True)
            print(f"Force closed {app_name}.exe using taskkill")
        except Exception as e:
            print(f"Taskkill failed: {e}")
