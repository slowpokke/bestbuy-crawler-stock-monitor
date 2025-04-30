import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ========== Config ==========
checking_interval = 30  # seconds between checks

# Enter your Discord Webhook Url here
DISCORD_WEBHOOK_URL = "*****" 

products = {
    "RTX 5070": "https://www.bestbuy.com/site/nvidia-geforce-rtx-5070-12gb-gddr7-graphics-card-graphite-grey/6614154.p?skuId=6614154",
    "RTX 5080": "https://www.bestbuy.com/site/nvidia-geforce-rtx-5080-16gb-gddr7-graphics-card-gun-metal/6614153.p?skuId=6614153",
    "9800": "https://www.bestbuy.com/site/amd-ryzen-7-9800x3d-8-core-16-thread-4-7-ghz-5-2-ghz-max-boost-socket-am5-unlocked-desktop-processor-silver/6606318.p?skuId=6606318",
}

# ========== Setup Selenium ==========
options = Options()
# options.add_argument("--headless")  # Enable for background mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ========== Discord Message ==========
def notify_discord(msg):
    if not DISCORD_WEBHOOK_URL:
        return
    payload = {
        "content": f"📦 {msg}"
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"📨 Discord notification sent: {msg}")
    except Exception as e:
        print(f"⚠️ Failed to send Discord notification: {e}")

# ========== Stock Monitor ==========
notified_items = set()  # Track items already notified

def check_stock():
    print(f"\n[{time.strftime('%H:%M:%S')}] Checking Stock...")

    for name, url in products.items():
        try:
            driver.get(url)

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Items are covered under")]'))
                )
            except:
                pass  # Continue even if not found

            add_btns = driver.find_elements(By.XPATH, '//button[@data-test-id="add-to-cart"]')
            in_stock = bool(add_btns)

            # Always print
            if in_stock:
                print(f"✅ {name} IN STOCK!")
                # Only notify if not already notified
                if name not in notified_items:
                    notify_discord(f"{name} is IN STOCK right now!")
                    notified_items.add(name)
            else:
                print(f"❌ {name} Out of stock.")
                # Reset status so it can notify next time again
                if name in notified_items:
                    notified_items.remove(name)

        except Exception as e:
            print(f"⚠️ {name} Check Failed: {e}")

# ========== Main Loop ==========
print("Starting product stock monitoring (Discord only)...")

try:
    while True:
        check_stock()
        time.sleep(checking_interval)
except KeyboardInterrupt:
    print("\n🛑 Program exited by user.")
    notify_discord("🚪 Monitor has been manually exited.")
    driver.quit()
