import json
from pathlib import Path
from dataclasses import field, dataclass
from typing import Dict, List, Any, Callable, Optional, Union, TypeVar

import aiohttp
from bs4 import BeautifulSoup
from rich.logging import RichHandler
from tenacity import retry, wait_exponential, stop_after_attempt

from utils.logger import Project_Logger
# from .proxy import ProxyManager, proxy_list

# Utils related import header.json 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
file_path = PROJECT_ROOT / "src/utils/header.json"

T = TypeVar('T')

# TODO doc everything from and all function (done)
# TODO add retry maximum (done)
# TODO fix logging in this script (done)

@dataclass
class ScraperResponse:
   status: int
   content: Any
   url: str
   headers: Dict[str, str] = field(default_factory=dict)
   error: Optional[str] = None

class BaseScraper:

   """
   Base scraper for token scraper ensuring easy to maintain and modularization

      Attributes:
         logger_name : Logger name for each script
   """
   
   def __init__(self, logger_name: str = __name__):

      """
      Initialize the Base scraper

         Args:
            logger_name (str): Logger name
      """

      self.logger = Project_Logger(logger_name)
      self.name = logger_name

      ...

   def get_header(self) -> Dict[str, str]:

      """
      Providing header for each specific scraper

         Args:
            header (json): An header for scraper
      """

      with open(file_path, 'r') as file:
         files = json.load(file)
         header = {
            'etherscan.io': files['ether'],
            'bscscan.io': files['bsc'],
            'solscan.io': files['sol']
         }
         return header.get(self.name, 'None')

   async def process_json(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Process response as JSON"""
        return await response.json()

   async def scrape(
      self, 
      url: str, 
      proccessor: Callable[[aiohttp.ClientResponse], T],
      ) -> ScraperResponse:

      """
      Custom asyncronous scraping using aiohttp and custom log

         Args:
            url (str): url given by user
            processor (Callable[[aiohttp.ClientResponse], T]): Output Processor such as, `text`, `json` and `soup_object`
      """

      if proccessor is None:
         proccessor = self.process_soup
   async def process_text(self, response: aiohttp.ClientResponse) -> str:
        """Process response as TEXT"""
        return await response.text()

   async def process_soup(self, response: aiohttp.ClientResponse) -> BeautifulSoup:
        """Process response as SOUP OBJECT"""
        text = await response.text()
        return BeautifulSoup(text, 'html5lib')

   def extract_element(self, soup):
      soup = BeautifulSoup(soup, 'html5lib')
      return soup

   async def scrape_element(
         self, 
         content: Optional[str] = None, 
         element: Optional[str] = None
         ) -> Any:
      
      """
      Scraping element from given html tag

         Args:
            content (str): Content of html tag
            element (str): Element of html tag

      Returning the element in list form
      """

      if content is None:
         return []
      soup = BeautifulSoup(content, 'html5lib')
      return [page for page in soup.select(element)] if element else []
      ...

   async def fetch(
      self, 
      session: aiohttp.ClientSession, 
      url: str, 
      processor: Callable[[aiohttp.ClientResponse], T],
      ) -> ScraperResponse: #type: ignore
      
      """
      Custom asyncronous fetching using aiohttp and custom log

         Args:
            session (iohttp.ClientSession): https client session
            url (str): url given by user
            processor (Callable[[aiohttp.ClientResponse], T]): Output Processor such as, `text`, `json` and `soup_object`
      """

      try: 
         async with session.get(
            url, 
            headers=self.get_header(), 
            ) as response:
            if response.status == 200:
               content = await processor(response) #type: ignore
               return ScraperResponse(
                  status=response.status,
                  content=content,
                  url=url,
                  headers=dict(response.headers)
               )
               print(response.headers)
            else:
               failed_msg = f"HTTP ERROR: {response.status} - {url}"
               self.logger.error(failed_msg)
               return ScraperResponse(
                  status=response.status,
                  content=None,
                  url=url,
                  headers=dict(response.headers)
               )
      except Exception as e:
         error_msg = f"FETCH FAILED {url}: {str(e)}"
         self.logger.info(error_msg)

   @retry(stop=stop_after_attempt(2), reraise=True)
   async def scrape(
      self, 
      url: str, 
      proccessor: Callable[[aiohttp.ClientResponse], T],
      ) -> ScraperResponse:

      """
      Custom asyncronous scraping using aiohttp and custom log

         Args:
            url (str): url given by user
            processor (Callable[[aiohttp.ClientResponse], T]): Output Processor such as, `text`, `json` and `soup_object`
      """

      if proccessor is None:
         proccessor = self.process_soup
         
      try:
         async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, url, proccessor)
            return response
      except Exception as error:
         error_msg = f"Session ERROR for {url}: {str(error)}"
         self.logger.error(error_msg)
         return ScraperResponse(
            status=0,
            content=None,
            url=url,
            error=error_msg
         )