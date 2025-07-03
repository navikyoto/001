import re
from collections import defaultdict

import asyncio

from scraper import BaseScraper
from .url_ import UrlManager

class EtherScan(BaseScraper):
   def __init__(self, address, use_proxies = False, logger_name = "etherscan.io"):
      super().__init__(use_proxies, logger_name)
      self.page = 1
      self.pages = []
      self.address = address
      self.url = self._url()
      self.holder: defaultdict = defaultdict(str)

   def _url(self):
      url = UrlManager(self.address, self.page)
      return url.construct_url()["holder"]

   async def return_(self, url, element) -> None:
      page = await self.scrape(url=url, proccessor=self.process_text)
      return await self.scrape_element(page.content, element)

   async def scrape_page(self):
      page = await self.scrape(url=self.url, proccessor=self.process_text)
      pages = await self.scrape_element(page.content,'span.page-link.text-nowrap')
      pages_num = [re.findall(r'[0-9]+', page.text) for page in pages]
      self.pages.append(int(pages_num[0][1]))

   async def scrape_info(self) -> None:
      await self.scrape_page()
      result = {}
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
      
      return self.holder
                  
tes = EtherScan("0x41D06390b935356b46aD6750bdA30148Ad2044A4")
print(asyncio.run(tes.scrape_info()))