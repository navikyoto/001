# Python3 program to extract all the numbers from a string
# import re

# # Function to extract all the numbers from the given string
# def getNumbers(str):
# 	array = re.findall(r'[0-9]+', str)
# 	return array

# # Driver code
# str = "Page 1 of 4"
# array = getNumbers(str)
# # print(*array)
# tes = int(array[1])

# # for i in range(tes):
# #    print(i+1)
# name = 'tes'
# txt3 = "My name is {name}, I'm {age}"
# tes = txt3.format(name=name, age='21')

# class satu():
#    def __init__(self, nama):
#       self.name = nama

# class dua(satu):
#    def tes(self):
#       print(self.name)

# sat = dua('tes')
# sat.tes()

# class Detections():
#     def __init__(self):
#         self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
#         self.page = []
#         self.url = 'https://etherscan.io/token/generic-tokenholders2?m=light&a={}&s=1000000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p={}'


#     def tes(self):
#         print(self.tokenAddress)

#     async def fetch(self,session, url):
#         async with session.get(url, headers = self.headers) as response:
#             html = await response.text()
#             return html


#     async def get_url(self):
#         async with aiohttp.ClientSession() as session:
#             content = await self.fetch(session, self.url.format(self.tokenAddress, 0))
#             soup = BeautifulSoup(content, 'lxml')
#             for page in soup.select('span.page-link.text-nowrap'):
#             array = re.findall(r'[0-9]+', page.text)
#             self.page.append(int(array[1]))


#     async def main(self):
#         await self.get_url()
#         for i in range(self.page[0]):
#             async with aiohttp.ClientSession() as session:
#             content = await self.fetch(session, self.url.format(self.tokenAddress, i+1))
#             soup = BeautifulSoup(content, 'lxml')
#             holders = '.d-flex.align-items-center.gap-1'
#             percents = '.progress-bar.bg-primary'
#             for holder,percent in zip(soup.select(holders), soup.select(percents)):
#                 print(f"{holder.text} :{percent['aria-valuenow']:%}")


#     def get_holder(self):
#         return asyncio.run(self.main())

# from utils.scrape import main, json_, text_
# url = 'https://api.dexscreener.com/token-pairs/v1/ethereum/0x41D06390b935356b46aD6750bdA30148Ad2044A4'

# main(url, json_)
# import csv
# import pandas as pd

# with open('file.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['name', 'age'])
#     writer.writerow(['John Doe', 30])

# pd.read_csv('stocks.csv')

# Output:
# The CSV file named 'file.csv' will be created and two rows of data will be written to it.

# from scraper.base_scraper import MainScrape

# import aiohttp
# from bs4 import BeautifulSoup
# from utils.logger import Project_Logger
# from dataclasses import field, dataclass
# from .proxy import proxy_list, ProxyManager
# from tenacity import retry, wait_exponential, stop_after_attempt
# from typing import Dict, List, Any, Callable, Optional, Union,TypeVar


# # TODO: Rapihkan
# # TODO: Line 53 error
# # TODO: Buat menjadi pendek
# # TODO: Jadikan class (done)

# T = TypeVar('T')

# @dataclass
# class ScraperResponse:
#    status: int
#    content: Any
#    url: str
#    headers: Dict[str, str] = field(default_factory=dict)
#    error: Optional[str] = None


# class BaseScraper:

#    def __init__(self, use_proxies: bool = True, logger_name: str = __name__):
#       self.proxy_manager = ProxyManager(proxy_list) if use_proxies else None
#       self.logger = Project_Logger(logger_name)
#       self.default_header = {
#          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
#          }

#    def get_header(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
#       if additional_headers:
#          return {**self.default_header, **additional_headers}
#       return self.additional_headers

#    async def process_json(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
#         """Process response as JSON"""
#         return await response.json()

#    async def process_text(self, response: aiohttp.ClientResponse) -> str:
#         """Process response as TEXT"""
#         return await response.text()

#    async def process_soup(self, response: aiohttp.ClientResponse) -> BeautifulSoup:
#         """Process response as SOUP OBJECT"""
#         text = await response.text()
#         return BeautifulSoup(text, 'html5lib')

#    async def extract_element(self, soup: BeautifulSoup, selector: str) -> List[Any]:
#       return soup.select(selector)

#    async def scrape_info_(self, content: str = None, element: str = None) -> None:
#       soup = BeautifulSoup(content, 'html5lib')
#       print(soup)
#       content = [page for page in soup.select(element)]
#       return content
#       ...

#    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
#    async def fetch(
#       self,
#       session: aiohttp.ClientSession,
#       url: str,
#       processor: Callable[[aiohttp.ClientResponse], T],
#       headers: Dict[str, str] = field(default_factory=dict),
#       timeout: int = 30,
#       ) -> ScraperResponse:
#       full_headers = self.get_header(headers)
#       proxy = self.proxy_manager.get_proxy() if self.proxy_manager else None

#       self.logger.info(f"fetching {url}")

#       try:
#          async with session.get(
#             url,
#             headers= full_headers,
#             proxy=proxy,
#             timeout= aiohttp.ClientTimeout(total=timeout)
#          ) as response:
#             if response.status == 200:
#                self.logger.info(f"Successfully fetched {url} (Status: {response.status})")
#                content = await processor(response)
#                return ScraperResponse(
#                   status=response.status,
#                   content=content,
#                   url=url,
#                   headers=dict(response.headers)
#                )
#             else:
#                error_msg = f"HTTP ERROR {response.status} for {url}"
#                self.logger.warning(error_msg)
#                return ScraperResponse(
#                   status=response.status,
#                   content=None,
#                   url=url,
#                   headers=dict(response.headers)
#                )
#       except Exception as e:
#          error_msg = f"Fetch failed for {url}: {str(e)}"
#          self.logger.error(error_msg)

#    async def scrape(
#       self,
#       url: str,
#       proccessor: Callable[[aiohttp.ClientResponse], T] = None,
#       headers: Optional[Dict[str, str]] = None,
#       timeout: int = 30
#    ) -> ScraperResponse:
#       if proccessor is None:
#          proccessor = self.process_soup

#       try:
#          self.logger.info(f"Starting scraping for {url}")
#          async with aiohttp.ClientSession() as session:
#             response = await self.fetch(
#                session=session,
#                url=url,
#                processor=proccessor,
#                headers=headers,
#                timeout=timeout
#             )
#             return response
#             print(response.content)
#       except Exception as error:
#          error_msg = f"Session ERROR for {url}: {str(error)}"
#          self.logger.error(error_msg)
#          return ScraperResponse(
#             status=0,
#             content=None,
#             url=url,
#             error=error_msg
#          )


# ether = "etherscan.io"
# bsc = "bscscan.io"

# def tes(arg):
#    match arg:
#       case 'ether':
#          return ether
#       case 'bsc':
#          return bsc

# tesi = tes('bsc')
# print(tesi)
# import json

# from utils.logger import Project_Logger


# class Tes():
#    def __init__(self, logger_name = __name__):
#       self.logger = Project_Logger(logger_name)
#       self.file = None

# class TesDua(Tes):
#    def __init__(self, logger_name = "etherscan.io"):
#       super().__init__(logger_name)
#       self.name = logger_name

#    def get_header(self):
#       with open('utils/header.json', 'r') as file:
#          tes = json.load(file)
#          header = {
#             'etherscan.io': tes['ether'],
#             'bscscan.io': tes['bsc']
#          }
#          return header.get(self.name, 'None')

# # print(self.name)
# ...
# with open('utils/header.json', 'r') as file:
#    self.file = json.load(file)
#    # print(self.file)
#    match self.name:
#       case('ether'):
#          print(self.file)
# return self.file['ether']

# # print(tes['ether'])
# ether = "etherscan.io"
# bsc = "bscscan.io"

# tes = TesDua()
# # print(tes["bsc"])

# print(tes.get_header())


# class UrlBuilder:
#    def __init__(self, base_url, address, page):
#       self.base_url = base_url
#       self.address = address
#       self.page = page
#       self.path = ""
#       self.params = {}

#    def with_path(self, path):
#       self.path = path
#       return self

#    def with_param(self, key, value):
#       self.params[key] = value
#       return self

#    def build(self):
#       url = self.base_url + self.path
#       if self.params:
#          url += "?" + "&".join(f"{k}={v}" for k, v in self.params.items())
#       return url

# # Usage
#    def construct_urls(self):

#       tokenomics_url = self.with_path(f"{self.address}") \
#                      .build()

#       holder_url = self.with_path("/generic-tokenholders2") \
#                   .with_param("m", "light") \
#                   .with_param("a", self.address) \
#                   .with_param("s", "1000000000000000000000000000") \
#                   .with_param("sid", "70069bba651b7c2c32ee067cd0ed8821") \
#                   .with_param("p", self.page) \
#                   .build()

#       return {
#          "base": self.base_url,
#          "tokenomics": tokenomics_url,
#          "holder": holder_url
#       }


# tes = UrlBuilder("https://bscscan.com/token/", "0xA49fA5E8106E2d6d6a69E78df9B6A20AaB9c4444", "1")
# holder = tes.construct_urls()
# print(holder['holder'])

# i = 0
# while True:
#    i += 1
#    print(f"https://api-v2.solscan.io/v2/token/holders?address=8SQQ1urC3Dynq9C2ieM6AozWgi4GCrLE6fnRoiWdpump&page_size=10&page={i}")

# holder = [

# ]

# from playwright.sync_api import sync_playwright
# playwright = sync_playwright().start()
# browser = playwright.chromium.launch(headless=False, slow_mo=100000)
# page = browser.new_page()
# header = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Alt-Used": "solscan.io",
#     "Connection": "keep-alive",
#     "Cookie": "cf_clearance=xk_.HcAACSFe7zDE35ebOIy0FdPnKuHbBDtuSrwIxeI-1750436961-1.2.1.1-14W.U8UE8x.7ZRzn4SNRxFfknfSwcTgJLCRqTFOha4VCuVOwyZDE5dpM80rs7V6DPyyr5Ws0U5MT3GZWQDOnxeUXFUELqNgceEtpT10rWmPf7OghM8syOvsF3cGVD1V4fG1TuDT0UQMBtKh8LINrAUeqZJFpmX.58vtYH5puCtSK638bloYGwIDlYPXWUxytA0QTl8JlNkYp.b7wIkmjab9XsGk2lgbh8f8BXn2EQWqZ8X_huaH11Vs3CRQqx5Kw2Ag.EvBWsbjYNW_VTgnq6rfc9sYzv.6EuOwTEYg1vr7_qaAh4lvf9tcoCo2QdEmM2y4.wCARenrYk8ks.48jpEwjdOlPIVTkGm75k7mXxzyusbwW20yV4bkBVpCw.GBX",
#     "DNT": "1",
#     "Priority": "u=0, i",
#     "Referer": "https://solscan.io/token/8Y5MwnUM19uqhnsrFnKijrmn33CmHBTUoedXtTGDpump?__cf_chl_tk=OPMQ4JvlYljsEWilUYpzO5Dca3EGC1PUhXs4tEzZFiA-1750436953-1.0.1.1-GwMfJ2j_fJyLEvXJyvfShHUG6daIwuMoAdmjHTvWFIg",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-GPC": "1",
#     "TE": "trailers",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
# }
# page.set_extra_http_headers(header)
# page.goto("https://solscan.io/token/8Y5MwnUM19uqhnsrFnKijrmn33CmHBTUoedXtTGDpump")
# span_locators = page.locator('span').all()
# # print(span_locators)
# for span_locator in span_locators:
#     span_locator.highlight()
#     text = span_locator.inner_text()
#     print(text)

# import requests
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import os

# valid_proxies = []

# with open('./proxy/http.txt', 'r') as file:
#     proxies = [p.strip() for p in file if p.strip()]

# def check_proxy(proxy):
#     try:
#         res = requests.get(
#             "https://ipinfo.io/json",
#             proxies={'http': proxy, 'https': proxy},
#             timeout=5
#         )
#         if res.status_code == 200:
#             print(proxy)
#             return proxy
#     except Exception:
#         pass
#     return None

# if __name__ == "__main__":
#     max_workers = min(32, (os.cpu_count() or 1) * 5)  # Tune as needed
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = [executor.submit(check_proxy, proxy) for proxy in proxies]
#         for future in as_completed(futures):
#             result = future.result()
#             if result:
#                 valid_proxies.append(result)

#     print(f"Valid proxies: {valid_proxies}")

import requests

with open('./proxy/valid.txt', 'r') as file:
    proxies = file.read().split('\n')
    
site_to_check = 'https://ipinfo.io/json'