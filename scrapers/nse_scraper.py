import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config.setting as settings
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def fii_dii_scraper():
    chrome_options = Options()
    if settings.Headless:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(settings.driver_path), options=chrome_options)
      # creating a new instance of the Chrome driver(it acts like a browser)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    data=[]
    try:
        driver.get(settings.buy_sell_URL)
        time.sleep(10)  # Let the page load completely
        tables = driver.find_elements(By.TAG_NAME, "table")
        target_table = None

        for table in tables:
            headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
            if "CATEGORY" in headers and "DATE" in headers:
                target_table = table
                break

        if not target_table:
            raise Exception("FII/DII table not found")
        
        rows = target_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip the header row
        for row in rows:
            # Fix: Using the correct By.TAG_NAME selector instead of string "tag name"
            cells = row.find_elements(By.TAG_NAME, "td")
            category = cells[0].text.strip()
            date_str = cells[1].text.strip()
            buy = float(cells[2].text.replace(',', '').replace(' ₹ Crores', ''))
            sell = float(cells[3].text.replace(',', '').replace(' ₹ Crores', ''))
            date = datetime.strptime(date_str, settings.DATE_FORMAT)
            data.append({'date': date, 'category': category, 'buy': buy, 'sell': sell})

        latest_date = max([d['date'] for d in data])
        latest_data = [d for d in data if d['date'] == latest_date]

        fii_data = next(d for d in latest_data if d['category'] == "FII/FPI")
        dii_data = next(d for d in latest_data if d['category'] == "DII")

        return {
            'date': latest_date,
            'fii_buying': fii_data['buy'],
            'fii_selling': fii_data['sell'],
            'dii_buying': dii_data['buy'],
            'dii_selling': dii_data['sell']
        }

    except Exception as e:
        print(f"Error while scraping: {e}")
        return None
    finally:
        driver.quit()
        # Close the browser

if __name__ == "__main__":
    result = fii_dii_scraper()
    if result:
        print(f"Scraped data for {result['date'].strftime(settings.DATE_FORMAT)}:")
        print(f"FII Buying: ₹{result['fii_buying']} Crores, Selling: ₹{result['fii_selling']} Crores")
        print(f"DII Buying: ₹{result['dii_buying']} Crores, Selling: ₹{result['dii_selling']} Crores")