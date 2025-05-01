import asyncio

from scraper import BaseScraper

class EtherScan(BaseScraper):
   def __init__(self, use_proxies = False, logger_name = "etherscan.io"):
      super().__init__(use_proxies, logger_name)
      self.url = self._url()

   def _url(self):
      return f"https://mangakatana.com"

   async def tes(self):
      page = await self.scrape(url=self.url, proccessor=self.process_text)
      # print(self.url)
      print(page)



tes = EtherScan()
asyncio.run(tes.tes())