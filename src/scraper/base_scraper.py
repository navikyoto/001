from dataclasses import field, dataclass
from typing import Dict, List, Any, Callable, Optional, Union,TypeVar

import aiohttp
from bs4 import BeautifulSoup
from tenacity import retry, wait_exponential, stop_after_attempt

from utils.logger import Project_Logger
from .proxy import ProxyManager, proxy_list


T = TypeVar('T')

@dataclass
class ScraperRenponse:
   status: int
   content: Any
   url: str
   headers: Dict[str, str] = field(default_factory=dict)
   error: Optional[str] = None

class BaseScraper:
   def __init__(self, use_proxies: bool = True, logger_name: str = __name__):
      self.proxy_manager = ProxyManager(proxy_list) if use_proxies else None