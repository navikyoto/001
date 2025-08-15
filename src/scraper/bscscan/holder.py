import re, os
from collections import defaultdict

import asyncio

# base_scraper and url_manager from own lib
from ..base_scraper import BaseScraper
from .url_ import UrlManager

class BscScan(BaseScraper):
   
   """
   Scraper of Binance token using own lib to scraper all necessary need.
		
		Attributes:
				address: Meme coin BEP-20 (Binance) Based address
				use_proxies: If True, use proxy for requests (default: False) currently not working
				logger_name: logger name, for addresing error
   """
         
   def __init__(self, address, use_proxies = False ,logger_name = "bscscan.io"):
      """
      Initialize the EtherScan scraper.
      
      Args:
         address (str): Binance token address to scrape
         use_proxies (bool, optional): Whether to use proxies. Defaults to False.
         logger_name (str, optional): Logger name. Defaults to "bscscam.io".
      """

      super().__init__(logger_name)
      self.page = 1
      self.pages = []        
      self.address = address
      self.url = self._url()
      self.holder: defaultdict = defaultdict(str)
      
   def _url(self):
      
      """
      Using `UrlManager` accepting two parameter `self.address` and `self.page`
	   and return holder address with a page.
      """

      tes = UrlManager(self.address, self.page)
      return tes.construct_url()["holder"]
   
   async def return_(self, url, element) -> None:
      
      """
      Returning element from a page, `proccessor` can be changed
      """

      page = await self.scrape(url=url, proccessor=self.process_text)
      return await self.scrape_element(page.content, element)
    
   # Perbarui cookies terlebih dahulu dari etherscan dan bscscan
    
   async def scrape_page(self):
      
      """
      Scraping page using `.scrape` from Basescraper and `.scrape_element` and return the total page.
      """

      try:

         self.logger.info(f"FETCHING: web pagination")
         page = await self.scrape(url=self.url, proccessor=self.process_text)
         
         if page.status == 200:
            pages = await self.scrape_element(page.content,'span.page-link.text-nowrap')
            pages_num = [re.findall(r'[0-9]+', page.text) for page in pages]
            self.pages.append(int(pages_num[0][1]))
            self.logger.info(f"SUCCESSFULLY FETCHED: {pages_num[0][1]} web pagination (STATUS: {page.status})")

         else:
            self.logger.error(f"FAILED FETCHING: HTTP ERROR {response.status}")

      except Exception as error:
         self.logger.warning(f"ERROR {str(error)}")

   async def scrape_info(self):

      """
      Scraping all info from all page that got scraped from scrape_page function
	   returning percantage and holder.
      """

      try:
         await self.scrape_page()
         self.logger.info(f"FETCHING INFORMATION: {self.pages[0]} url")
         result = {}
         for pages in range(self.pages[0]):
            self.page = pages+1
            self.url = self._url()
            response = await self.scrape(url=self.url, proccessor=self.process_text)
            if response.status == 200:
               task = [
                  self.return_(self.url, '.d-flex.align-items-center.gap-1'),
                  self.return_(self.url, 'tbody.align-middle.text-nowrap .progress-bar.bg-primary'),
               ]
               
               holders, percentages = await asyncio.gather(*task)
               holder = [str(holder.text).strip() for holder in holders]
               # print(holder)
               result.update({
                  self.extract_element(str(holder)).text: str(percent['aria-valuenow'])
                  for holder, percent in zip(holder, percentages)
               })
               self.holder = result
            else:
               self.logger.error(f"FETCHED FAILED: {response.status}")

         self.logger.info(f"SUCCESSFULLY FETCHED INFORMATION: {self.pages[0]} url (STATUS: {response.status})")
         
         # os.system("clear")   
         return self.holder
      except Exception as error:
         self.logger.warning(f"ERROR {str(error)}")

# asyncio.run(tes.scrape_page())
if __name__ == "__main__":
   tes = BscScan('0xA49fA5E8106E2d6d6a69E78df9B6A20AaB9c4444')
   asyncio.run(tes.scrape_info())
   ...
# print(asyncio.run(tes.scrape_info()))