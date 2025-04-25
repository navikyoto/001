import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List
from dataclasses import field    
from .proxy import proxy_list, ProxyManager
from ..utils.logger import logging


# TODO: Rapihkan
# TODO: Line 53 error
# TODO: Buat menjadi pendek
# TODO: Jadikan class (done)


class BaseScraper:

   def __init__(self):
      self.proxy_manager = ProxyManager(proxy_list)

   def header(self):
      return {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}


   def json_(self,response: str) -> None:
      return response.json()

   def text_(self, response: dict) -> None:
      return response.text()

   def soup(self, soup: str) -> None:
      return BeautifulSoup(soup, 'html5lib')

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
