from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# Checking interval in seconds
checking_interval = 1

# Your Bark Key
BARK_KEY = "******"

# Target product list
products = {
    "RTX 5070": "https://www.bestbuy.com/site/nvidia-geforce-rtx-5070-12gb-gddr7-graphics-card-graphite-grey/6614154.p?skuId=6614154",
    "RTX 5080": "https://www.bestbuy.com/site/nvidia-geforce-rtx-5080-16gb-gddr7-graphics-card-gun-metal/6614153.p?skuId=6614153"
}

# Set up browser
options = Options()
# options.add_argument("--headless")  # Uncomment to run without opening browser
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Send Bark notification
def notify_bark(msg):
    if not BARK_KEY:
        return
    url = f"https://api.day.app/{BARK_KEY}/{msg}"
    try:
        requests.get(url)
        print(f"📲 Bark notification sent: {msg}")
    except Exception as e:
        print(f"⚠️ Failed to send Bark notification: {e}")

# Main stock checking function
def check_stock():
# notify_bark(" Test message: Script is running") 
    print(f"\n[{time.strftime('%H:%M:%S')}] Checking Stock...")
    for name, url in products.items():
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            buttons = driver.find_elements(By.XPATH, '//button[contains(text(),"Add to Cart")]')

            if buttons:
                print(f"✅ {name} IN STOCK!")
                notify_bark(f"{name} is IN STOCK right now!")
            else:
                print(f"❌ {name} Out of stock...")
        except Exception as e:
            print(f"⚠️ {name} Check Failed: {e}")

# Start monitoring loop
print("Start checking your target list...")
while True:
    check_stock()
    time.sleep(checking_interval)
