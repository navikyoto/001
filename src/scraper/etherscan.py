import re
import asyncio
from .base_scraper import BaseScraper
from utils.logger import Project_Logger

class EtherScan(BaseScraper):
   def __init__(self, address, ):
      self.page = 1
      self.pages_ = []
      self.holder = []
      self.address = address
      self.url = self._url()
      self.logger = Project_Logger()
      
   def _url(self):
      return f'https://etherscan.io/token/generic-tokenholders2?m=light&a={self.address}&s=100000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p={self.page}'
   
   async def return_(self, content: str, element: str) -> None:
      page = await self.scrape(content, self.process_text, headers=self.default_header)
      return await self.scrape_info_(page, element)
     
   @property
   async def get_url(self) -> None:
      return await self.scrape(self.url, self.process_text)

   async def scrape_page(self) -> None:
        pages = await self.scrape_info_(await self.get_url, 'span.page-link.text-nowrap')
        print(pages)
      #   page = [re.findall(r'[0-9]+', page.text) for page in pages]
      #   self.pages_.append(int(page[0][1]))
      
   def run(self):
      return asyncio.run(self.scrape_page())
   
tes = EtherScan('0x41D06390b935356b46aD6750bdA30148Ad2044A4')
tes.run()