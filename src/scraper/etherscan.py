import re
from collections import defaultdict

import asyncio
from bs4 import BeautifulSoup

from scraper import BaseScraper

class EtherScan(BaseScraper):
   def __init__(self, address, use_proxies = False, logger_name = "etherscan.io"):
      super().__init__(use_proxies, logger_name)
      self.page = 1
      self.pages = []
      self.address = address
      self.url = self._url()
      self.holder: defaultdict = defaultdict(str)

   def _url(self):
      return f'https://etherscan.io/token/generic-tokenholders2?m=light&a={self.address}&s=100000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p={self.page}'

   async def return_(self, url, element) -> None:
      page = await self.scrape(url=url, proccessor=self.process_text)
      return await self.scrape_element(page.content, element)

   async def scrape_page(self):
      self.logger.info(f"Starting to scraping page {self.url}")
      page = await self.scrape(url=self.url, proccessor=self.process_text)
      pages = await self.scrape_element(page.content,'span.page-link.text-nowrap')
      pages_num = [re.findall(r'[0-9]+', page.text) for page in pages]
      self.pages.append(int(pages_num[0][1]))

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
                  


tes = EtherScan("0x41D06390b935356b46aD6750bdA30148Ad2044A4")
asyncio.run(tes.scrape_info())
# for key, value in holder.items():
#    print(key, value)