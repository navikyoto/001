import re, os
from pathlib import Path

import asyncio
import pandas as pd

# base_scraper and url_manager from own lib
from scraper import BaseScraper
from .url_ import UrlManager
from .tokenomics import tknomics

# Renew the cookies through header.json for etherscan before running the script!
class EtherScan(BaseScraper):

   """
   Scraper of Binance token using own lib, to scrape token information.
		
		Attributes:
				address: Meme coin ERC-20 (Ethereum) based address.
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
      self.tokenomics = tknomics(self.address)

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

      eth = await self.tokenomics.scrape_page()
      files = f"../src/result/eth - {eth[0].name}.csv" #type: ignore

      hold_acc = []

      try:

         # Checking if file already exists
         if Path(files).exists():
            os.system("clear")
            self.logger.info("FILE ALREADY EXISTS")

         else:
            # Updating the scrape_page() function
            await self.scrape_page()
            self.logger.info(f"FETCHING INFORMATION: {self.pages[0]} url")

            # 
            for pages in range(self.pages[0]):
               self.page = pages+1
               self.url = self._url()
               response = await self.scrape(url=self.url, proccessor=self.process_text)
               if response.status == 200:

                  # Element of holders, quantity, percentages, and value
                  task = [
                     self.return_(self.url, '.d-flex.align-items-center.gap-1 a.js-clipboard.link-secondary'),
                     self.return_(self.url, 'tbody.align-middle.text-nowrap tr td:nth-of-type(3) span[data-bs-toggle]'),
                     self.return_(self.url, 'tbody.align-middle.text-nowrap .progress-bar.bg-primary'),
                     self.return_(self.url, 'tbody.align-middle.text-nowrap tr td:nth-of-type(5)')
                  ]
                  
                  holders, quantity, percentages, values = await asyncio.gather(*task)

                  items = zip(holders, quantity, percentages, values) if values else zip(holders, quantity, percentages)

                  for i, elems in enumerate(items):
                     hold, qty, perc, *val = elems
                     data = {
                        "address": self.extract_element(str(hold["data-clipboard-text"])).text,
                        "quantity": self.extract_element(str(qty)).text,
                        "percetages": str(perc['aria-valuenow']),
                     }
                     hold_acc.append(data)

                     if val:  # only if values exist
                        data["value"] = self.extract_element(str(val[0])).text
                        hold_acc.append(data)

               else:
                  self.logger.error(f"FETCHED FAILED: {response.status}")
                  
            if not values: #type: ignore
               self.logger.info("THIS TOKEN HAS NO VALUE")

            self.logger.info(f"SUCCESSFULLY FETCHED INFORMATION: {self.pages[0]} url (STATUS: {response.status})") #type: ignore

            df = pd.DataFrame(hold_acc)
            df.to_csv(files) 

            self.logger.info("FILE SAVED SUCCESSFULLY IN result FOLDER")

      except Exception as error:
         self.logger.warning(f"ERROR {str(error)}")

if __name__ == "__main__":
   tes = EtherScan("0x41D06390b935356b46aD6750bdA30148Ad2044A4")
   asyncio.run(tes.scrape_info())