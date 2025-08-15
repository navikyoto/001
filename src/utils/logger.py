import logging, os

import aiohttp
from rich.logging import RichHandler

from tenacity import retry, wait_exponential, stop_after_attempt

# coloredlogs.install(level='DEBUG')

logging.basicConfig(
         level= logging.INFO,
         format="%(message)s",
         datefmt="[%X]",
         handlers=[RichHandler(rich_tracebacks=True, markup=True, enable_link_path=False)]
      )

class Project_Logger():
   def __init__(self, logger_name):
      
      # logging.basicConfig(
      #    level = logging.INFO,
      #    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
      #    datefmt = "%d/%m/%y - [%H:%M:%S]",
      #    handlers= [RichHandler()]
      # )

      self.logger = logging.getLogger(logger_name)
      file_handler = logging.FileHandler(f"{logger_name}.log")
      self.logger.addHandler(file_handler)

      # return self.logger


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
         self.logger.error(f"Fetish failed: {e}")
         raise

   def info(self, massage: str) -> None:
      # os.system('clear')
      self.logger.info(massage)

   def error(self, massage: str) -> None:
      # os.system('clear')

      self.logger.error(massage)

   def warning(self, massage: str) -> None:
      # os.system('clear')
      self.logger.warning(massage)