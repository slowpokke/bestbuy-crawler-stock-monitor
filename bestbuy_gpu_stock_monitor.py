from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests


#Checking Interval
checking_interval = 30

#Your Bark Device Token (Bark key)
Enter_Your_Bark_Key_Here = "******"


#Target List
products = {
    "RTX 5070": "https://www.bestbuy.com/site/nvidia-geforce-rtx-5070-12gb-gddr7-graphics-card-graphite-grey/6614154.p?skuId=6614154",
    "RTX 5080": "https://www.bestbuy.com/site/nvidia-geforce-rtx-5080-16gb-gddr7-graphics-card-gun-metal/6614153.p?skuId=6614153"
}

BARK_KEY = Enter_Your_Bark_Key_Here

#Initializing browser using webdriver
options = Options() 
options.add_argument("--headless")  # #This if you need to see the browser page
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def notify_bark(msg):
    if not BARK_KEY:
        return
    url = f"https://api.day.app/{BARK_KEY}/{msg}"
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(text(),"Add to Cart")]'))
        )
        # Wait at most 10s for loading, else pass
    except:
        pass  

def check_stock():
    print(f"\n[{time.strftime('%H:%M:%S')}] Checking Stock...")
    for name, url in products.items():
        try:
            driver.get(url)
            time.sleep(5)

            buttons = driver.find_elements(By.XPATH, '//button[contains(text(),"Add to Cart")]')

            if buttons:
                print(f"✅ {name} IN STOCK!")
                notify_bark(f"{name} Is IN STOCK right know!!!")
            else:
                print(f"❌ {name} Out of stock...")
        except Exception as e:
            print(f"{name} Check Failed: {e}")

print("Start checking your target list...")
while True:
    check_stock()
    time.sleep(checking_interval)

