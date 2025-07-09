import asyncio
import aiohttp

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

asyncio.run(main(url))

# with open("../valid.txt", "r") as file:
#    proxies = file.read().split("\n")
   
# async def fetch(url, session, proxy, semaphore):
#    async with semaphore:
#       async with session.get(url, proxy=f"http://{proxy}") as response:
#          return await response.status

# async def main(url):
#    max_concurrent_requests = 10
#    semaphore = asyncio.Semaphore(max_concurrent_requests)
#    async with aiohttp.ClientSession() as session:
#       #  tasks = []
#       for proxy in proxies:
#          task = [fetch(url, session, proxy, semaphore)]
#          result = await asyncio.gather(*task)
#          print(result)

# asyncio.run(main("https://solscan.io/token/8Y5MwnUM19uqhnsrFnKijrmn33CmHBTUoedXtTGDpump"))