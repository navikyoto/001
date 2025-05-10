import re
import json
from dataclasses import dataclass
from collections import defaultdict

import asyncio
import requests
from bs4 import BeautifulSoup

from scraper import BaseScraper
from .url_ import UrlManager


header = {
   "accept-encoding": "gzip, deflate, br, zstd",
   "cookie": "bscscan_offset_datetime=+7; ASP.NET_SessionId=cpqaadlkuq1wv5dswbh34wew; bscscan_switch_token_amount_value=value; bscscan_cookieconsent=True; __cflb=02DiuJNoxEYARvg2sN6bbkRgdyaaxAA7EHVmAeSPBe5jA; cf_clearance=W1xPZduen3p3zl9t_mjGNZsBpV8Ul6Xjt5USH7zQRsk-1746849233-1.2.1.1-jT3N.kAiqbikfrly0w4E1g8A0WdIyo7_7Ah6tKxQGoomDc0HXz2_0TWLtsA8IEpcXt4l0g9VYgClVNoulePABWOXMn10W0kRRGLnv1PKqKbcld1IUQvnghsRPQNQJAcTVhER2fgn8Mhs0sUxmEWiDyrWa6fkyBqkEGsVYXog69uaZJDIWFAyb.Mgy0t5arj2XxyKfNTRB6HiXuEafVCGHfi6bOnRAdKCAPErYFVfi6.Q9B67YAcyZd9oOXp6YecVPVJC_zvXBGVvbUvxX0yMCuKDAq7NtC3TzzL0_rWw2zlCZfggr9vkRot2oR9dh88zvByVvWvL4m4b.0bdb6KIAaICULAXBu4aQRSuIsDtV0XMDi7QhaM.rka7yq6dJivA",
   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

@dataclass
class Data:
   price: int
   holder: str
   total_transfers: str
   token_contract: str
   max_total_supply: str
   onchain_market_cap: str
   circulating_supply_market_cap: str

class BscScan(BaseScraper):
   def __init__(self, address, use_proxies = False ,logger_name = "bscscan.io"):
      super().__init__(use_proxies, logger_name)
      self.address = address
      self.url = self._url()
      
   def _url(self):
      url = UrlManager(self.address)
      return url.construct_url()['tokenomics']
   
   def scrape_page(self):
      with open('utils/header.json', 'r') as file:
         files = json.load(file)
      # print(files["bsc"])
      req = requests.get(self.url, headers=files['bsc']).text
      soup = BeautifulSoup(req, 'html5lib')
      print(soup)
      # page = await self.scrape(url=self.url, proccessor=self.process_text)
      # print(page.content)
   
tes = BscScan("0xA49fA5E8106E2d6d6a69E78df9B6A20AaB9c4444")
# asyncio.run(tes.scrape_page())
print(tes.scrape_page())