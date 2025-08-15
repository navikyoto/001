import re
import json
from dataclasses import dataclass
from collections import defaultdict

import asyncio
from bs4 import BeautifulSoup

from scraper import BaseScraper
from .url_ import UrlManager

@dataclass
class Tokenomics:
   price: int
   holder: str
   total_transfers: str
   token_contract: str
   max_total_supply: str
   onchain_market_cap: str
   circulating_supply_market_cap: str

class BscScan(BaseScraper):

   """
   Scraper anything related to Token information from website

      Attributes:
         address: Meme coin BEP-20 (Binance) Based address.
         use_proxies: If True, use proxy for requests (default: False) currently not working.
         logger_name: Logger name, for addresing error.

   """

   def __init__(self, address, logger_name = "bscscan.io"):
      
      """
      Initialize the BscScan scraper

      Args:
         address (str): Binance token address to scrape.
         use_proxies (bool, optional): Whetever to use proxies. Defaults to False.
         logger_name(str, optional): Logger name. Defaults to "bscscan.io"
      """

      super().__init__(logger_name)
      self.address = address
      self.url = self._url()
      
   def _url(self):

      """
      Using `UrlManager` accepting two parameter `self.address` and `self.page`
	   and return holder address with a page.
      """

      url = UrlManager(self.address)
      return url.construct_url()['tokenomics']
   
   async def return_(self, page, element):

      """
      Returning element from a page, `proccessor` can be changed
      """

      data = await self.scrape_element(page.content, element)
      return data[0].text.strip()

   async def scrape_page(self):

      """
      Fetching information from bscscan.io and return information such as
         Args:
            price: An price of token.
            holder: Address holder.
            total_transfer: Total trasfer of token.
            token_contract: Token contract.
            max_total_supply: Total supply of token.
            onchain_market_cap: Market cap onchain.
            circulating_supply_market_cap: Supply circulating on the market.
      """

      try:
         page = await self.scrape(url=self.url, proccessor=self.process_text)
         if page.status == 200:
            self.logger.info(f"FETCHING INFORMATION")
            return Tokenomics(
               price = await self.return_(page, '.card.h-100 span[data-bs-html=true]'),
               holder = await self.return_(page, '.d-flex.flex-wrap.gap-2 div'),
               total_transfers = await self.return_(page, 'div #totaltxns'),
               token_contract = await self.return_(page, 'a.text-truncate.d-block'),
               max_total_supply = await self.return_(page, 'div span.hash-tag.text-truncate'),
               onchain_market_cap = await self.return_(page, '#ContentPlaceHolder1_tr_marketcap div'),
               circulating_supply_market_cap = await self.return_(page, '#ContentPlaceHolder1_tr_marketcap div'),
            ), self.logger.info(f"SUCCESSFULLY FETCHED INFORMATION: (STATUS: {page.status})")
         else:
            self.logger.error(f"FETCHING FAILED: {page.status}")


      except Exception as error:
         self.logger.error(f"ERROR {str(error)}")

if __name__ == "__main__":
   tes = BscScan("0xAaEE2036cD24203e907d34F4b188977d4c20f4B3")
   print(asyncio.run(tes.scrape_page()))