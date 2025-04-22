import aiohttp
import asyncio
import requests
import concurrent.futures
from bs4 import BeautifulSoup

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
      soup = BeautifulSoup(content, 'lxml')
      
      ip_address = soup.select('.table-responsive .table.table-striped.table-bordered tbody tr td:first-child')
      port_address = soup.select('.table-responsive .table.table-striped.table-bordered tbody tr td:nth-of-type(2)')
      http_type = soup.select('.table-responsive .table.table-striped.table-bordered tbody tr td:nth-of-type(7)')
      
      for ip, port, http in zip(ip_address, port_address, http_type):
            proxy = f"https://{ip.text}:{port.text}" if http.text == 'yes' else f"http://{ip.text}:{port.text}"
            proxy_list.append(proxy)
            # print(proxy)
            
# async def filter_proxy():
#    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
   

                    
asyncio.run(main())
# print(len(proxy_list))