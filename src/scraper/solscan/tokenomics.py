import re
from dataclasses import dataclass
from collections import defaultdict

import asyncio
import pandas
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from scraper import BaseScraper
from .url_ import UrlManager

@dataclass
class Tokenomics:
    price: int
    holder: str
    creator: str
    decimals: int
    first_mint: str
    token_contract: str
    total_transfers: str
    max_total_supply: str
    onchain_market_cap: str


class SolScan(BaseScraper):
    def __init__(self, address, use_proxies=False, logger_name="solscan.io"):
        super().__init__(use_proxies, logger_name)
        self.address = address
        self.url = self._url()
        
    def _url(self):
        url = UrlManager(self.address)
        return url.construct_url()["tokenomics"]
    
    async def scrape_page(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=False)
            page = await browser.new_page()

            await page.set_extra_http_headers(self.get_header())
            await page.goto(self.url, wait_until='networkidle')
            await page.wait_for_load_state('networkidle')

            content = await page.content()
            soup = BeautifulSoup(content, 'html5lib')

            price = soup.select_one('.card.h-100 span[data-bs-html=true]')
    
tes = SolScan("8Y5MwnUM19uqhnsrFnKijrmn33CmHBTUoedXtTGDpump")
print(tes.url)