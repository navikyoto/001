from dataclasses import dataclass
from collections import defaultdict

import asyncio

from scraper import BaseScraper
from .url_ import UrlManager

@dataclass
class Tokenomics:
   name: str
   price: int
   holder: str
   total_transfers: str
   token_contract: str
   max_total_supply: str
   onchain_market_cap: str
   circulating_supply_market_cap: str

class tknomics(BaseScraper):
   def __init__(self, address, use_proxies = False ,logger_name = "etherscan.io"):
      super().__init__(logger_name)
      self.address = address
      self.url = self._url()
      
   def _url(self):
      url = UrlManager(self.address)
      return url.construct_url()['tokenomics']
   
   async def return_(self, page, element):
      data = await self.scrape_element(page.content, element)
      return data[0].text.strip()

   async def scrape_page(self):

      """
      Fetching information from bscscan.io and return information such as
         Args:
            name: Name of token
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
            return [Tokenomics(
               name = await self.return_(page, 'section.container-xxl span.fs-base.fw-medium'),
               price = await self.return_(page, '.card.h-100 span[data-bs-html=true]'),
               holder = await self.return_(page, '.d-flex.flex-wrap.gap-2 div'),
               total_transfers = await self.return_(page, 'div#ContentPlaceHolder1_trNoOfTxns'),
               token_contract = await self.return_(page, 'a.text-truncate.d-block'),
               max_total_supply = await self.return_(page, 'div span.hash-tag.text-truncate'),
               onchain_market_cap = await self.return_(page, '#ContentPlaceHolder1_tr_marketcap div'),
               circulating_supply_market_cap = await self.return_(page, '#ContentPlaceHolder1_tr_marketcap div')
            ), self.logger.info(f"SUCCESSFULLY FETCHED INFORMATION: (STATUS: {page.status})")]
      
         else:
            self.logger.error(f"FETCHING FAILED: {page.status}")

      except Exception as error:
         self.logger.error(f"ERROR {str(error)}")
