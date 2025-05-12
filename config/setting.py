import os 
#scraper settings
buy_sell_URL=os.getenv('BUY_SELL_URL',"https://www.nseindia.com/reports/fii-dii")
driver_path = "/opt/homebrew/bin/chromedriver"
Headless = os.getenv('HEADLESS', 'True').lower() == 'true'
DATE_FORMAT = os.getenv("DATE_FORMAT", "%d-%b-%Y")  # Matches "09-May-2025"
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")