import asyncio

from scraper import BaseScraper

class EtherScan(BaseScraper):
   def __init__(self, address, use_proxies = False, logger_name = "etherscan.io"):
      super().__init__(use_proxies, logger_name)
      self.pages = 1
      self.address = address
      self.url = self._url()

   def _url(self):
      return f'https://etherscan.io/token/generic-tokenholders2?m=light&a={self.address}&s=100000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p={self.pages}'

   async def scrape_page(self):
      page = await self.scrape(url=self.url, proccessor=self.process_text)
      # pages = await self.scrape_element(page,'span.page-link.text-nowrap')
      print(page)


tes = EtherScan("0x41D06390b935356b46aD6750bdA30148Ad2044A4")
asyncio.run(tes.scrape_page())