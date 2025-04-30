from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# Time interval between checks (in seconds)
checking_interval = 5

# Your Bark push key
BARK_KEY = "****"

# Target products to monitor
products = {
    "RTX 5070": "https://www.bestbuy.com/site/nvidia-geforce-rtx-5070-12gb-gddr7-graphics-card-graphite-grey/6614154.p?skuId=6614154",
    "RTX 5080": "https://www.bestbuy.com/site/nvidia-geforce-rtx-5080-16gb-gddr7-graphics-card-gun-metal/6614153.p?skuId=6614153",
}

# Chrome browser options
options = Options()
# options.add_argument("--headless")  # Uncomment to hide browser window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Bark push notification
def notify_bark(msg):
    if not BARK_KEY:
        return
    url = f"https://api.day.app/{BARK_KEY}/{msg}"
    try:
        requests.get(url)
        print(f"📲 Bark notification sent: {msg}")
    except Exception as e:
        print(f"⚠️ Failed to send Bark notification: {e}")

# Check stock for all products
def check_stock():
    print(f"\n[{time.strftime('%H:%M:%S')}] Checking Stock...")
    for name, url in products.items():
        try:
            driver.get(url)

            # Wait for "Items are covered under" — skip silently if not found
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Items are covered under")]'))
                )
            except:
                pass  # Skip wait if the phrase doesn't appear

            # Check for "Add to Cart" button
            add_btns = driver.find_elements(By.XPATH, '//button[@data-test-id="add-to-cart"]')

            if add_btns:
                print(f"✅ {name} IN STOCK!")
                notify_bark(f"{name} is IN STOCK right now!")
            else:
                print(f"❌ {name} Out of stock.")

        except Exception as e:
            print(f"⚠️ {name} Check Failed: {e}")

# Start the monitoring loop
print("🚀 Starting product stock monitoring...")
while True:
    check_stock()
    time.sleep(checking_interval)
