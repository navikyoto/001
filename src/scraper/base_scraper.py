import aiohttp
from bs4 import BeautifulSoup
from ..utils.logger import Project_Logger
from dataclasses import field, dataclass    
from .proxy import proxy_list, ProxyManager
from typing import Dict, List, Any, Callable, Optional, Union,TypeVar


# TODO: Rapihkan
# TODO: Line 53 error
# TODO: Buat menjadi pendek
# TODO: Jadikan class (done)


@dataclass
class ScraperResponese:
   status: int
   content: Any
   url: str
   headers: Dict[str, str] = field(default_factory=dict)
   error: Optional[str] = None


class BaseScraper:

   def __init__(self, use_proxies: bool = True, logger_name: str = __name__):
      self.proxy_manager = ProxyManager(proxy_list) if use_proxies else None
      self.logger = Project_Logger(logger_name)
      self.default_header = {
         'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
         }

   def get_header(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
      if additional_headers:
         return {**self.default_header, **additional_headers}
      return self.additional_headers

   async def process_json(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Process response as JSON"""
        return await response.json()

   async def process_text(self, response: aiohttp.ClientResponse) -> str:
        """Process response as JSON"""
        return await response.text()

   async def process_soup(self, response: aiohttp.ClientResponse) -> BeautifulSoup:
        """Process response as JSON"""
        text = await response.text()
        return BeautifulSoup(text, 'html5lib')

   async

   async def scrape_info_(self, content: str = None, element: str = None) -> None:
      soup = BeautifulSoup(content, 'html5lib')
      print(soup)
      content = [page for page in soup.select(element)]
      return content
      ...

   async def fetch(
      self,
      session: aiohttp.ClientSession, 
      url: str, 
      headers: Dict[str, str] = field(default_factory=dict),
      output: str = None,
      ) -> None:
      async with session.get(url, headers = self.header(), proxy=self.proxy_manager.get_proxy()) as response:
         return await output(response)
         ...   
         
   async def main(self, url: str, output: str | list, headers = None ) -> None:
      try:
         async with aiohttp.ClientSession() as session:
            content = await self.fetch(session, url, headers = headers, output = output)
            print("Scraping of token") 
            return content
      except Exception as error:
         print(f"Error while scraping token: {error}")
