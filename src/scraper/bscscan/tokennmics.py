import re
from collections import defaultdict

import asyncio

from scraper import BaseScraper
from .url_ import UrlManager

class BscScan(BaseScraper):
   
