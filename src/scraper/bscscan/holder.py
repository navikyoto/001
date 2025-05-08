import re
from urllib.parse import urljoin, urlencode
from collections import defaultdict

import asyncio

from scraper import BaseScraper

class BscScan(BaseScraper):
   def __init__(self, address, logger_name = "bscscan.io"):
      super().__init__(logger_name)
      self.page = 1
      self.pages = []
      self.address = address
      self.url = self._url()
      self.holder: defaultdict = defaultdict(str)
      
   def build_url(self):
      return {
         "base": "https://bscscan.com/token/",
         "tokenmics" : f"{self.address}#tokenInfo",
         "holder" : f"generic-tokenholders2?m=light&a={self.address}&s=1000000000000000000000000000&sid=70069bba651b7c2c32ee067cd0ed8821&p={self.page}"
      }
      #return f'https://bscscan.com/token/generic-tokenholders2?m=light&a={self.address}&s=1000000000000000000000000000&sid=70069bba651b7c2c32ee067cd0ed8821&p={self.page}'
   
   def tes(self):
      print(f"{self.url['base']}{self.url['holder']}")
   
   async def return_(self, url, element) -> None:
      page = await self.scrape(url=url, proccessor=self.process_text)
      return await self.scrape_element(page.content, element)
    
   async def scrape_page(self):
      page = await self.scrape(url=self.url, proccessor=self.process_text)
      pages = await self.scrape_element(page.content,'span.page-link.text-nowrap')
      pages_num = [re.findall(r'[0-9]+', page.text) for page in pages]
      self.pages.append(int(pages_num[0][1]))
      # print(int(pages_num[0][1]))
      
   async def scrape_info(self) -> None:
      await self.scrape_page()
      result = {}
      # print(self.pages[0])
      for pages in range(self.pages[0]):
         self.page = pages+1
         self.url = self._url()
         task = [
            self.return_(self.url, '.d-flex.align-items-center.gap-1'),
            self.return_(self.url, 'tbody.align-middle.text-nowrap .progress-bar.bg-primary')
         ]
         
         holders, percentages = await asyncio.gather(*task)
         holder = [str(holder.text).strip() for holder in holders]
         # print(holder)
         result.update({
            self.extract_element(str(holder)).text: str(percent['aria-valuenow'])
            for holder, percent in zip(holder, percentages)
         })
         self.holder = result
         # print(self.holder)
         for key, value in self.holder.items():
            print(key, value)
      
      return self.holder
      
tes = BscScan('0xA49fA5E8106E2d6d6a69E78df9B6A20AaB9c4444', 'bsc')
tes.tes()
#asyncio.run(tes.scrape_info())