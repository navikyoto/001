import logging
import aiohttp
from tenacity import retry, wait_exponential, stop_after_attempt

class Project_Logger():
   def __init__(self, logger_name):
      logging.basicConfig(
         level = logging.INFO,
         format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
         datefmt = "%d/%m/%y - [%H:%M:%S]"
      )
      
      self.logger = logging.getLogger(logger_name)
      file_handler = logging.FileHandler(f"{logger_name}.log")
      self.logger.addHandler(file_handler)
      
      
   @retry(stop = stop_after_attempt(3),
          wait = wait_exponential(multiplier = 1, min = 4, max = 10))
   async def fetching_retry(self, url: str) -> None:
      try:
         async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
               if response.status == '200':
                  self.logger.info(f"Successfully fetched {url}")
                  return await response.text()
               else:
                  self.logger.warning(f"Non-200 response: {response.status}")
                  return None
      except Exception as e:
         self.logger.error(f"Fetch failed: {e}")
         raise
      
   def info(self, massage: str) -> None:
      self.logger.info(massage)
      
   def error(self, massage: str) -> None:
      self.logger.error(massage)
      
   def warning(self, massage: str) -> None:
      self.logger.warning(massage)