from src.scraper.base_scraper import BaseScraper

class Etherscanner(BaseScraper):
   def __init__(self):
      super().__init__(
         base_url=f'https://etherscan.io/token/generic-tokenholders2?m=light&a={self.address}&s=100000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p={self.page}'
         
      )