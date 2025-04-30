# GPU Stock Sentinel

Lately, I’ve been trying to buy a GPU, but it’s hard to keep checking the site manually all the time. So I built this simple stock tracker that automatically monitors GPU availability on BestBuy.

Since BestBuy has pretty strong anti-bot protections, I used Selenium to simulate real browser behavior and bypass JavaScript-based defenses. While it’s relatively slow (because it loads full pages), I think it’s good enough for tracking products that aren’t extremely competitive to purchase.

You can easily customize it by modifying the `products` list in the script to monitor different items of your choice.

## Features
- Auto-checks RTX 5070 / 5080 pages every 10s
- Uses headless Chrome via Selenium to bypass anti-bot protections *Slow but effective*
- Sends push notifications to your phone when stock is detected

## Python Environment
- selenium
- webdriver-manager
- requests

## Bark App
- Copy the key behind : https://api.day.app/

# Notice
This is a simple Python script that monitors stock availability for BestBuy products and sends a push notification using Bark.

It works by checking for the presence of an **"Add to Cart"** button on the product page.  
If the phrase **"Items are covered under..."** appears below the button (as it usually does), the detection is highly accurate.

If that line does not exist on the page, detection **may** fail or throw an error.  
However, this method works reliably for **most BestBuy products**.
