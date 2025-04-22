import aiohttp
from typing import Dict, List
from dataclasses import field
from bs4 import BeautifulSoup
from utils.logger import Project_Logger

logger = Project_Logger()

# TODO: Perlu di tambah informasi token di line 42

def json_(response: str) -> None:
   return response.json()

def text_(response: dict) -> None:
   return response.text()

HEADER = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}

def soup(soup: str) -> None:
   return BeautifulSoup(soup, 'lxml')

async def scrape_info_(content: str = None, element: str = None) -> None:
   soup = BeautifulSoup(content, 'lxml')
   content = [page for page in soup.select(element)]
   return content
   ...

async def fetch(
   session: aiohttp.ClientSession, 
   url: str, 
   headers: Dict[str, str] = field(default_factory=dict),
   output: str = None
   ) -> None:
   async with session.get(url, headers = headers) as response:
      return await output(response)
      ...   
      
async def main(url: str, output: str | list, headers = None ) -> None:
   try:
      async with aiohttp.ClientSession() as session:
         content = await fetch(session, url, headers = headers, output = output)
         logger.info("Scraping of token") 
         return content
   except Exception as error:
      logger.error(f"Error while scraping token: {error}")
