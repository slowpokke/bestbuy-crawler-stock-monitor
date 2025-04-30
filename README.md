#  GPU Stock Sentinel (BestBuy Optimized)

Lately, I’ve been trying to buy a GPU, but it’s hard to keep checking the site manually all the time. So I built this simple stock tracker that automatically monitors GPU availability on BestBuy.

This version is **specifically optimized for BestBuy**. It efficiently detects product stock status by directly checking for the presence of an **“Add to Cart”** button, which is a reliable indicator across most BestBuy product pages.

##  Features

- Auto-checks selected BestBuy product pages every 30 seconds
- Efficiently detects stock for **most GPUs and tech items**
- Simulates real user behavior with Selenium to bypass anti-bot mechanisms
- Sends **push notifications to your phone** via Bark (optional)
- Sends **Discord messages to your own server** (see `discord_*.py` version)

##  How It Works

This script uses Selenium to open product pages in a real browser session (Chrome), waits briefly for the page to load, then searches for an **Add to Cart** button.

> 💡 If this button is present, the item is considered **in stock**.

It avoids fragile page structure assumptions and works even if BestBuy’s layout changes slightly.

##  Notifications (Optional)

You can choose from two notification methods:

- **Bark**: Sends instant push notifications to your iPhone via the Bark app  
- **Discord**: Newer version (`discord_*.py`) allows you to send messages directly to a channel on your personal Discord server

##  Requirements

- Python 3.8+
- `selenium`
- `webdriver-manager`
- `requests`

Install dependencies:

```bash
pip install selenium webdriver-manager requests
