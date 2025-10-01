import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import logging

logging.getLogger('selenium').setLevel(logging.WARNING)

chrome_option = Options()
# Try running with headless disabled for more reliable results
chrome_option.add_argument("--headless")  # <- You can comment this to debug
chrome_option.add_argument("--disable-blink-features=AutomationControlled")
chrome_service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service, options=chrome_option)

def get_internet_speed():
    try:
        driver.get("https://fast.com/")
        
        # Wait for "Show more info" link, indicating test is done
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, 'show-more-details-link'))
        )
        
        # Now wait until speed-value is non-zero
        for _ in range(30):
            speed_value = driver.find_element(By.ID, 'speed-value').text.strip()
            if speed_value and speed_value != "0":
                return speed_value + " Mbps"
            time.sleep(1)  # wait and check again

        return "Speed value did not update in time."

    except Exception as e:
        return f"Error: {e}"

print("Speed:", get_internet_speed())
driver.quit()
