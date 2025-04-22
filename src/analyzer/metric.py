import requests
import cloudscraper
from bs4 import BeautifulSoup
from src.scraper.proxy import proxy_list


HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
for proxy in proxy_list:
   proxys = {'http': proxy, 'https': proxy}
   scraper = cloudscraper.create_scraper(browser = {"browser" : 'chrome', "platform" : 'windows', "desktop" : True})
   print(scraper.get('https://dexscreener.com/solana/5naj2assh2tnjvzuxwzrqhqwovnuawkj1jzaiafsvg95', proxies = proxys).text)