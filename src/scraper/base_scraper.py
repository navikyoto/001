import aiohttp
from bs4 import BeautifulSoup
from utils.logger import Project_Logger
from dataclasses import field, dataclass    
from .proxy import proxy_list, ProxyManager
from tenacity import retry, wait_exponential, stop_after_attempt
from typing import Dict, List, Any, Callable, Optional, Union,TypeVar


# TODO: Rapihkan
# TODO: Line 53 error
# TODO: Buat menjadi pendek
# TODO: Jadikan class (done)

T = TypeVar('T')

@dataclass
class ScraperResponse:
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
        """Process response as TEXT"""
        return await response.text()

   async def process_soup(self, response: aiohttp.ClientResponse) -> BeautifulSoup:
        """Process response as SOUP OBJECT"""
        text = await response.text()
        return BeautifulSoup(text, 'html5lib')

   async def extract_element(self, soup: BeautifulSoup, selector: str) -> List[Any]:
      return soup.select(selector)

   async def scrape_info_(self, content: str = None, element: str = None) -> None:
      soup = BeautifulSoup(content, 'html5lib')
      print(soup)
      content = [page for page in soup.select(element)]
      return content
      ...

   @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
   async def fetch(
      self,
      session: aiohttp.ClientSession, 
      url: str,
      processor: Callable[[aiohttp.ClientResponse], T],
      headers: Dict[str, str] = field(default_factory=dict),
      timeout: int = 30,
      ) -> ScraperResponse:
      full_headers = self.get_header(headers)
      proxy = self.proxy_manager.get_proxy() if self.proxy_manager else None
      
      self.logger.info(f"fetching {url}")
         
      try:
         async with session.get(
            url,
            headers= full_headers,
            proxy=proxy,
            timeout= aiohttp.ClientTimeout(total=timeout)
         ) as response:
            if response.status == 200:
               self.logger.info(f"Successfully fetched {url} (Status: {response.status})")
               content = await processor(response)
               return ScraperResponse(
                  status=response.status,
                  content=content,
                  url=url,
                  headers=dict(response.headers)
               )
            else:
               error_msg = f"HTTP ERROR {response.status} for {url}"
               self.logger.warning(error_msg)
               return ScraperResponse(
                  status=response.status,
                  content=None,
                  url=url,
                  headers=dict(response.headers)
               )
      except Exception as e:
         error_msg = f"Fetch failed for {url}: {str(e)}"
         self.logger.error(error_msg)
   
   async def scrape(
      self,
      url: str,
      proccessor: Callable[[aiohttp.ClientResponse], T] = None,
      headers: Optional[Dict[str, str]] = None,
      timeout: int = 30
   ) -> ScraperResponse:
      if proccessor is None:
         proccessor = self.process_soup

      try:
         self.logger.info(f"Starting scraping for {url}")
         async with aiohttp.ClientSession() as session:
            response = await self.fetch(
               session=session,
               url=url,
               processor=proccessor,
               headers=headers,
               timeout=timeout
            )
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