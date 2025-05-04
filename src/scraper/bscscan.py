import re
from collections import defaultdict

import asyncio
from bs4 import BeautifulSoup

from scraper import BaseScraper

class BscScan(BaseScraper):
   def __init__(self, address, use_proxies = False, logger_name = "bscscan.io"):
      super().__init__(use_proxies, logger_name)
      self.page = 1
      self.pages = []
      self.address = address
      self.url = self._url()
      self.holder: defaultdict = defaultdict(str)
      
   def _url(self):
      return f'https://bscscan.com/token/{self.address}#balances'
      
   async def scrape_page(self):
      page = await self.scrape(url=self.url, proccessor=self.process_text)
      print(page.headers)
      
tes = BscScan('0xA49fA5E8106E2d6d6a69E78df9B6A20AaB9c4444')
asyncio.run(tes.scrape_page())