import time
import random
import asyncio
from typing import List
import concurrent.futures
from datetime import datetime, timedelta

import aiohttp
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# TODO: Filter proxy 

async def fetch(session, url):
   async with session.get(url) as response:
      html = await response.text()
      return html
      
proxy_list = []

async def main():
   url = 'https://free-proxy-list.net/'
   async with aiohttp.ClientSession() as session:
      content = await fetch(session, url)
      soup = BeautifulSoup(content, 'html5lib')
      
      ip_address = soup.select('.table-responsive .table.table-striped.table-bordered tbody tr td:first-child')
      port_address = soup.select('.table-responsive .table.table-striped.table-bordered tbody tr td:nth-of-type(2)')
      http_type = soup.select('.table-responsive .table.table-striped.table-bordered tbody tr td:nth-of-type(7)')
      
      for ip, port, http in zip(ip_address, port_address, http_type):
            proxy = f"https://{ip.text}:{port.text}" if http.text == 'yes' else f"http://{ip.text}:{port.text}"
            proxy_list.append(proxy)

asyncio.run(main())


def filter_proxy(proxy: str):
   if not proxy.startswith(('http://', 'https://')):
      proxy = f"http://{proxy}"

      start_time = time.time()      
      proxies = {
         'http': proxy,
         'https': proxy
      }
   
   try:
      response = requests.get(
         "http://etherscan.io",
         proxies=proxies,
         timeout=10
      )

      response_time = time.time() - start_time

      if response.status_code == 200:
         return proxy, True, response_time
      else:
         return "FALSE"
         #return proxy, False, response_time

   except Exception as e:
      return "ERROR"


#for proxy in proxy_list:
#   print(filter_proxy(proxy))


class ProxyManager:
   
   def __init__(self, proxy: List['str']):
      self.proxies = proxy
      self.current_proxies = []
      self.last_rotation_time = datetime.now()
      self._proxy_rotation()

   def _proxy_rotation(self):
      self.current_proxies = self.proxies.copy()
      random.shuffle(self.current_proxies)
      self.last_rotation_time = datetime.now()
      print(f"Proxies rotated at {self.last_rotation_time}")

   def get_proxy(self) -> str:
      if datetime.now() - self.last_rotation_time >= timedelta(minutes=30):
         self._proxy_rotation()

      return random.choice(self.current_proxies)

   async def check_rotation(self):
      while True:
         if datetime.now() - self.last_rotation_time >= timedelta(minutes=30):
            self._proxy_rotation()
         await asyncio.sleep(60)