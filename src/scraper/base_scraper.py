from dataclasses import field, dataclass
from typing import Dict, List, Any, Callable, Optional, Union,TypeVar

import aiohttp
from bs4 import BeautifulSoup
from tenacity import retry, wait_exponential, stop_after_attempt

from utils.logger import Project_Logger
from .proxy import ProxyManager, proxy_list


T = TypeVar('T')

@dataclass
class ScraperResponse:
   status: int
   content: Any
   url: str
   headers: Dict[str, str] = field(default_factory=dict)
   error: Optional[str] = None

class BaseScraper:
   def __init__(self, use_proxies: bool = False, logger_name: str = __name__):
      self.proxy_manager = ProxyManager(proxy_list) if use_proxies else None
      self.logger = Project_Logger(logger_name)
      self.default_header = {
         "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
         "accept-encoding": "gzip, deflate, br, zstd",
         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
         "sec-ch-ua": 'Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135',
         "referer": 'https://etherscan.io/token/generic-tokenholders2?m=light&a=0x41D06390b935356b46aD6750bdA30148Ad2044A4&s=100000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p=1&__cf_chl_tk=vonScrp03nlcYA2n_B3.sTTHc31puGF.glyAPKifXK8-1746254426-1.0.1.1-FFjaPr4SJF6.KRGC05oX9Cq5IkyYAsb78P888pYlu_8',
         "origin": "https://etherscan.io",
         "cookie": "etherscan_offset_datetime=+7; etherscan_cookieconsent=True; __stripe_mid=a6e9107e-cac4-4851-9633-176a96576fb803631e; cards-currentTab=all; etherscan_switch_token_amount_value=value; _ga=GA1.2.1428820244.1740546000; _ga_T1JC9RNQXV=GS1.1.1741144315.8.0.1741144315.60.0.0; ASP.NET_SessionId=cc44aivmwdxlvzlq32dufgy5; __cflb=02DiuFnsSsHWYH8WqVWoFjjPeFuLMdcb9ddWcEqxuzmpg; cf_clearance=tilcxCH.ek9faq7Tc7hq5Hs.v04g.vofbrGhN4AsgFo-1746254440-1.2.1.1-lc_pKSLYp0BVjyaxh0c6EYGApkN8A7mzbcYFShSqEiPSf5nWbv8YBZ1zimf912vsDdQ8J0Qb9LiijIW7jNShdad1FX1qHNuz9svnpWlCTN2ICLylWsuW37nlbulbXi8dSUpLd9cPoWLKCnMtaDQHraqf.IjHFDgzEEiTMFiSjT_q.dgDNoZtbj8zUf2FtpUfeRJxO4VUerQsh_EI8QSUibSyGEx25aH6lz.ySPafoeE6viOI2tHzfj.IfoYYJVBuMx4Rsfu4flTc976Me8UHCk7lIk4tAJ46GPdvag5AHWTuq0y6Ab4kxNhGdnJYildASHIRXBoutLPmE_LOh1pk2De44EOBgK3wpX2oxig.WU7ryScun014Z7Z4FuqtrjqQ"
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

   async def scrape_element(self, content: str = None, element: str = None) -> None:
      soup = BeautifulSoup(content, 'html5lib')
      print(soup)
      # content = [page for page in soup.select(element)]
      # return content
      ...a

   async def fetch(
      self, 
      session: aiohttp.ClientSession, 
      url: str, 
      processor: Callable[[aiohttp.ClientResponse], T],
      header: Dict[str, str] = field(default_factory=dict)
      ) -> ScraperResponse:
      self.logger.info(f"FETCHING: {url}")
      
      full_header = self.get_header(header) if header else self.default_header
      proxy = self.proxy_manager.get_proxy() if self.proxy_manager else None
      
      try: 
         async with session.get(
            url, 
            headers=full_header, 
            proxy=proxy
            ) as response:
            if response.status == 200:
               self.logger.info(f"SUCCESSFULLY FETCHED: {url} (STATUS: {response.status})")
               content = await processor(response)
               # return response.headers
               return ScraperResponse(
                  status=response.status,
                  content=content,
                  url=url,
                  headers=dict(response.headers)
               )
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
            
   async def scrape(
      self, 
      url: str, 
      proccessor: Callable[[aiohttp.ClientResponse], T] = None,
      header: Optional[Dict[str, str]] = None
      ) -> ScraperResponse:
      if proccessor is None:
         proccessor = self.process_soup
         
      try:
         self.logger.info(f"STARTING SCRAPING: {url}")
         async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, url, proccessor, header)
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