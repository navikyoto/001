import threading
from concurrent.futures import ThreadPoolExecutor

import asyncio
import aiohttp


# TODO Scrape dari banyak website dan masukan dalam list
# TODO Ambil banyak dan taruh di dalam proxy_list.txt
# TODO Filter proxy secepatnya
# TODO Save ke filter_proxy.txt
# TODO check file tersebut sudah di buat atau tidak


thread_local = threading.local()

url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"

async def fetch_proxies(url, session):
   async with session.get(url) as response:
      if response.status == 200:
         proxy_list = await response.text()
         print(f"total proxies fetched: {len(proxy_list)}")
         return proxy_list
      else:
         print(f"Failed to fetch proxies: {response.status}")

async def main(url):
   async with aiohttp.ClientSession() as session:
      proxies = await fetch_proxies(url, session)
      if proxies:
         with open("./proxy/fetched.txt", "w") as file:
            file.write(proxies)
         print("Proxies saved to fetched.txt")
      else:
         print("No proxies fetched.")

# asyncio.run(main(url))

# import asyncio

# import aiohttp

# with open("./proxy/fetched.txt", "r") as file:
#    proxies = file.read().split("\n")


# async def fetch(s, proxy):
#    async with s.get("http://ipinfo.io/json", proxy=f"http://{proxy}") as r:
#       if r.status != 200:
#          r.raise_for_status()
#       return await r.text()

# async def fetch_all(s):
#    tasks = []
#    for proxy in proxies:
#       task = asyncio.create_task(fetch(s, proxy))
#       tasks.append(task)
#    res = await asyncio.gather(*tasks)
#    return res

# async def main():
#    async with aiohttp.ClientSession() as session:
#       html = await fetch_all(session)
#       print(html)


# if __name__ == '__main__':
#    asyncio.run(main())

import asyncio
import aiohttp

# Load proxies from file
with open("./proxy/fetched.txt", "r") as file:
   proxies = [p.strip() for p in file if p.strip()]
   # for p in file:
   #    if p.strip():
   #       p.strip()
         # print(file.read().split('\n'))

async def fetch(session, proxy):
   try:
      async with session.get("http://ipinfo.io/json", proxy=f"http://{proxy}") as response:
         if response.status != 200:
            raise aiohttp.ClientError(f"Non-200 status: {response.status}")
         response.raise_for_status()
         text = await response.text()
         print(f"[✓] Success: {proxy}")
         return text
   except Exception as e:
        return None

async def fetch_all(session):
    tasks = [fetch(session, proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    return [res for res in results if res is not None]

async def main():
    async with aiohttp.ClientSession() as session:
        results = await fetch_all(session)
        print(f"\n[✓] {len(results)} successful responses out of {len(proxies)} proxies.")

if __name__ == '__main__':
    asyncio.run(main())













# from proxy_checker import ProxyChecker

# checker = ProxyChecker()

# def checking_proxy(proxies):
#    for proxy in proxies:
#       if checker.check_proxy(proxy) != False:
#          print(checker.check_proxy(proxy))
#       else:
#          ...

# threading.Thread(target=checking_proxy(proxies)).start()
#  checking_proxy(proxies)


# async def fetch(url, session, proxy, semaphore):
#    async with semaphore:
#       async with session.get(url, proxy=f"http://{proxy}") as response:
#          return await response.status

# async def main(url):
#    max_co*ncurrent_requests = 10
#    semaphore = asyncio.Semaphore(max_concurrent_requests)
#    async with aiohttp.ClientSession() as session:
#       #  tasks = []
#       for proxy in proxies:
#          task = [fetch(url, session, proxy, semaphore)]
#          result = await asyncio.gather(*task)
#          print(result)

# asyncio.run(main("https://solscan.io/token/8Y5MwnUM19uqhnsrFnKijrmn33CmHBTUoedXtTGDpump"))