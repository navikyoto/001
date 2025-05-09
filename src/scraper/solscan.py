import re
import asyncio
from collections import defaultdict

from bs4 import BeautifulSoup

from scraper import BaseScraper

class SolScan(BaseScraper):
   def __init__(self, address, use_proxies = False, logger_name = "solscan.io"):
      super().__init__(use_proxies, logger_name)
      self.page = 1
      self.pages = []
      self.address = address
      self.url = self._url()
      self.holder: defaultdict = defaultdict(str)
      
   def _url(self):
      return f'https://etherscan.io/token/generic-tokenholders2?m=light&a={self.address}&s=100000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p={self.page}'

   async def scrape_page(self):
      self.logger.info(f"Starting to scraping page {self.url}")
      page = await self.scrape(url=self.url, proccessor=self.process_text)
      cd