import logging, os

import aiohttp
from rich.logging import RichHandler

from tenacity import retry, wait_exponential, stop_after_attempt

# Basic configuration for logging
logging.basicConfig(
         level= logging.INFO,
         format="%(name)s - %(message)s",
         datefmt="[%X]",
         handlers=[RichHandler(rich_tracebacks=True, markup=True, enable_link_path=False)]
      )

class Project_Logger():
   def __init__(self, logger_name):

      self.logger = logging.getLogger(logger_name)
      file_handler = logging.FileHandler(f"{logger_name}.log")
      self.logger.addHandler(file_handler)

   @retry(stop = stop_after_attempt(3),
          wait = wait_exponential(multiplier = 1, min = 4, max = 10))
   async def fetching_retry(self, url: str) -> None:
      try:
         async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
               if response.status == 200:
                  self.logger.info(f"Successfully fetched {url}")
                  return await response.text()
               else:
                  self.logger.warning(f"Non-200 response: {response.status}")
                  return None
      except Exception as e:
         self.logger.error(f"Fetish failed: {e}")
         raise

   def info(self, massage: str, *args, **kwargs) -> None:
      self.logger.info(massage, *args, stacklevel=2, **kwargs)

   def error(self, massage: str, *args, **kwargs) -> None:
      self.logger.error(massage, args, stacklevel=2, **kwargs)

   def warning(self, massage: str, *args, **kwargs) -> None:
      self.logger.warning(massage, *args, stacklevel=2, **kwargs)