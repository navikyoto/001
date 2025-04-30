from scraper import BaseScraper

class EtherScan(BaseScraper):
   def __init__(self, use_proxies = True, logger_name = "etherscan.io"):
      super().__init__(use_proxies, logger_name)