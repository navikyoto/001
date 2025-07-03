from dataclasses import dataclass
from collections import defaultdict

import asyncio

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
   def __init__(self, address, use_proxies = False ,logger_name = "etherscan.io"):
      super().__init__(use_proxies, logger_name)
      self.address = address
      self.url = self._url()
      
   def _url(self):
      url = UrlManager(self.address)
      return url.construct_url()['tokenomics']
   
   async def return_(self, page, element):
      data = await self.scrape_element(page.content, element)
      return data[0].text.strip()

   async def scrape_page(self):
      page = await self.scrape(url=self.url, proccessor=self.process_text)
      # print(page)
      return Tokenomics(
         price = await self.return_(page, '.card.h-100 span[data-bs-html=true]'),
         holder = await self.return_(page, '.d-flex.flex-wrap.gap-2 div'),
         total_transfers = await self.return_(page, 'div#ContentPlaceHolder1_trNoOfTxns'),
         token_contract = await self.return_(page, 'a.text-truncate.d-block'),
         max_total_supply = await self.return_(page, 'div span.hash-tag.text-truncate'),
         onchain_market_cap = await self.return_(page, '#ContentPlaceHolder1_tr_marketcap div'),
         circulating_supply_market_cap = await self.return_(page, '#ContentPlaceHolder1_tr_marketcap div')
      )
   
tes = BscScan("0x41D06390b935356b46aD6750bdA30148Ad2044A4")
print(asyncio.run(tes.scrape_page()))