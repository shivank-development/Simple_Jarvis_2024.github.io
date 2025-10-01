import time
import csv
import json
import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style, init as colorama_init
from stt import speak  # ✅ using your module instead of pyttsx3

# ================== CONFIG ==================
THRESHOLD_DOWNLOAD = 20  # Mbps
THRESHOLD_UPLOAD = 5     # Mbps
CSV_FILE = "internet_speed_log.csv"
JSON_FILE = "internet_speed_log.json"
MAX_RETRIES = 3          # Retry if test fails
# ============================================

# Setup
logging.getLogger('selenium').setLevel(logging.WARNING)
colorama_init(autoreset=True)

chrome_option = Options()
chrome_option.add_argument("--headless=new")  # Latest Chrome headless mode
chrome_option.add_argument("--disable-blink-features=AutomationControlled")
chrome_option.add_argument("--window-size=1920,1080")
chrome_option.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_option.add_argument("--log-level=3")  # Suppress most Chrome logs
chrome_service = ChromeService(ChromeDriverManager().install())


def wait_for_non_zero_value(driver, by, value_id, timeout=60):
    """Wait until a given element has a non-zero value."""
    for _ in range(timeout):
        try:
            element = driver.find_element(by, value_id)
            text = element.text.strip()
            if text and text != "0":
                return text
        except:
            pass
        time.sleep(1)
    return "0"


def get_full_speed_metrics(driver):
    """Fetch speed metrics from fast.com."""
    try:
        driver.get("https://fast.com/")

        show_more = WebDriverWait(driver, 90).until(
            EC.element_to_be_clickable((By.ID, 'show-more-details-link'))
        )
        show_more.click()
        time.sleep(1)

        download = wait_for_non_zero_value(driver, By.ID, 'speed-value')
        upload = wait_for_non_zero_value(driver, By.ID, 'upload-value')
        latency = wait_for_non_zero_value(driver, By.ID, 'latency-value')

        return {
            "Download": float(download),
            "Upload": float(upload),
            "Latency": float(latency)
        }

    except Exception as e:
        return {"Error": str(e)}


def log_to_csv(data):
    """Log speed test results to CSV file."""
    is_new = False
    try:
        with open(CSV_FILE, 'r'):
            pass
    except FileNotFoundError:
        is_new = True

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["Timestamp", "Download (Mbps)", "Upload (Mbps)", "Latency (ms)"])
        writer.writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data["Download"],
            data["Upload"],
            data["Latency"]
        ])


def log_to_json(data):
    """Log results to JSON for structured storage."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "download": data["Download"],
        "upload": data["Upload"],
        "latency": data["Latency"]
    }
    try:
        with open(JSON_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    logs.append(entry)
    with open(JSON_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def check_and_alert(data):
    """Check thresholds and issue alerts."""
    alerts = []
    if data["Download"] < THRESHOLD_DOWNLOAD:
        alerts.append(f"Download speed low: {data['Download']} Mbps")
    if data["Upload"] < THRESHOLD_UPLOAD:
        alerts.append(f"Upload speed low: {data['Upload']} Mbps")

    if alerts:
        full_msg = " | ".join(alerts)
        print(Fore.RED + "⚠️ ALERT:", full_msg)
        speak(full_msg)   # ✅ using your speak function
    else:
        print(Fore.GREEN + "✅ Internet speed is above threshold.")
        speak("Internet speed is good")


def run_test():
    """Run speed test with retries (single execution)."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with webdriver.Chrome(service=chrome_service, options=chrome_option) as driver:
                data = get_full_speed_metrics(driver)

            if "Error" not in data:
                print(
                    f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] "
                    f"{Style.BRIGHT}Speed Test Result:"
                )
                print(
                    f"Download: {Fore.CYAN}{data['Download']} Mbps{Style.RESET_ALL} | "
                    f"Upload: {Fore.CYAN}{data['Upload']} Mbps{Style.RESET_ALL} | "
                    f"Latency: {Fore.YELLOW}{data['Latency']} ms"
                )
                log_to_csv(data)
                log_to_json(data)
                check_and_alert(data)
                return
            else:
                raise Exception(data["Error"])
        except Exception as e:
            print(Fore.RED + f"❌ Attempt {attempt} failed:", str(e))
            if attempt < MAX_RETRIES:
                time.sleep(5)

    print(Fore.RED + "❌ All attempts failed. Exiting.")


if __name__ == "__main__":
    print(Style.BRIGHT + Fore.MAGENTA + "______Internet Speed Monitor Started._______")
    run_test()   # ✅ Run only once