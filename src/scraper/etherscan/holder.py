import re, os
from collections import defaultdict

import asyncio

# base_scraper and url_manager from own lib
from scraper import BaseScraper
from .url_ import UrlManager

# Renew the cookies through header.json for etherscan before running the script!
class EtherScan(BaseScraper):

   """
   Scraper of Binance token using own lib, to scrape token information.
		
		Attributes:
				address: Meme coin ERC-20 (Ethereum) Based address.
				use_proxies: If True, use proxy for requests (default: False) currently not working.
				logger_name: logger name, for addresing error.
   """
   
   def __init__(self, address, use_proxies = False ,logger_name = "etherscan.io"):

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

      url = UrlManager(self.address, self.page)
      return url.construct_url()["holder"]

   async def return_(self, url, element) -> list:
            
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

         else:
            self.logger.error(f"FAILED FETCHING: HTTP ERROR {page.status}")
      
      except Exception as error:
         self.logger.warning(f"ERROR {str(error)}")

   async def scrape_info(self) -> None:
      
      """
      Scraping all info from all page that got scraped from scrape_page function
	   returning percantage and holder.

         Args:
            percentage (str): An percentages of token hold by user.
            holder (str): Holder token address.
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
            else:
               self.logger.error(f"FETCHED FAILED: {response.status}")
         
         self.logger.info(f"SUCCESSFULLY FETCHED INFORMATION: {self.pages[0]} url (STATUS: {response.status})")
         return self.holder
      
      except Exception as error:
         self.logger.warning(f"ERROR {str(error)}")

if __name__ == "__main__":
   tes = EtherScan("0x41D06390b935356b46aD6750bdA30148Ad2044A4")
   print(asyncio.run(tes.scrape_info()))
   ...