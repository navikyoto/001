import abc
import aiohttp
from dataclasses import dataclass
from utils.logger import Project_Logger
from typing import List, Dict, Optional


@dataclass
class TokenConfig:
    chainID: str
    tokenAddress: str


class BaseScraper(abc.ABC):
    def __init__(
        self,
        base_url: str,
        config: TokenConfig
    ):
        """
        Constructor untuk scraper

        Args:
            base_url (str): Link dari website yang akan di scraping 
            config: chainID dan token address dari crypto yang akan di scrape
        """

        self.session = None
        self.config = config
        self.base_url = base_url

    async def __aenter__(self):
        """
        Metode async context manager
        Membuat session aiohttp
        """

        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        """
        Closing session
        """

        if self.session:
            await self.session.close()

    async def fetch(
        self,
        url: str,
        method: str = 'GET',
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        url (string): URL untuk scrape/fetch
        method (str): GET or POST
        headers (optional): Kustom headers
        params (optional): Parameters quert
        """

        logger = Project_Logger()
        
        try:
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                'Accept': 'application/json'
            }

            headers = {**default_headers, **(headers or {})}

            async with self.session.request(
                method,
                url,
                headers=headers,
                params=params,
            ) as response:
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientError as e:
            logger.error(f"Fetch error {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error {e}")
            return None
        
        raise NotImplementedError
    
    @abc.abstractmethod
    async def scrape(self) -> List[Dict]:
        """
        Metode abstrak untuk scraping
        Wajib di-override di child class
        """
        pass
    