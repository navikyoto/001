import asyncio
from typing import Optional
from dataclasses import dataclass
from utils.logger import Project_Logger
from scraper.ethereum import Detections
from scraper.info_scrape import Info, info_, link
# from scraper.base_scraper import MainScrape

@dataclass
class Main:
   chainID: str
   tokenAddress: str

   async def info(self) -> Optional[dict]:
      try:
         logger = Project_Logger()
         info = Info(self.chainID, self.tokenAddress)
         logger.info(f"Fetching information of token: {self.tokenAddress}")
         
         # response = self.logger.fetching_retry()
         # print(link())
         
         return await info_(info)
      except Exception as error:
         logger.error(f"Error while fetching token information: {error}")
         return None
      
   def detections(self):
      detect = Detections(self.tokenAddress)
      return detect.run()

if __name__ == '__main__':
   info = Main(chainID = 'ethereum', tokenAddress =  '0x41D06390b935356b46aD6750bdA30148Ad2044A4')
   # main = MainScrape(chainID = 'ethereum', tokenAddress =  '0x41D06390b935356b46aD6750bdA30148Ad2044A4')
   asyncio.run(info.info())
   print(info.detections())