import aiohttp
import asyncio
import random
from bs4 import BeautifulSoup
from proxy import proxy_list

semaphore = asyncio.Semaphore(10)
HEADER = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

# async def filter_proxy(proxy):
#    target_url = 'https://dexscreener.com'
#    try:
#       async with aiohttp.ClientSession() as session:
#          async with session.get(target_url, proxy = proxy, timeout = 5, ssl = False) as respones:
#             if respones.status == 200:
#                print(f"Proxy Ok: {proxy}")
#                return proxy
#             else:
#                print(f"Proxy Error: {proxy.status}")
#    except Exception as e:
#       return None

# async def fetch(url, proxy):
#    async with semaphore:
#       try:
#          # proxy = random.choice(proxy_list)
#          # timeout = aiohttp.ClientTimeout(total = 30, connect = 10)
#          async with aiohttp.ClientSession(trust_env = True, headers = HEADER) as session:
#             async with session.get(url, proxy = proxy, timeout = 10,  ssl = False) as response:
#                if response.status == 200:
#                   print(f"Success scraping with proxy: {proxy}")
#                   return await response.text()
#                else:
#                   print(f"Failed scraping with proxy: {proxy}")
#                   return None
#       except aiohttp.ClientHttpProxyError:
#          return None
#       except aiohttp.client_exceptions.ClientProxyConnectionError:
#          return None
      
   
# async def main():
#    url = 'https://dexscreener.com/solana/5naj2assh2tnjvzuxwzrqhqwovnuawkj1jzaiafsvg95'
   
#    valid_proxies = await asyncio.gather(*(filter_proxy(proxy) for proxy in proxy_list))
#    valid_proxies = [proxy for proxy in valid_proxies if proxy]
   
#    if not valid_proxies:
#       print("No valid proxies found")
#       return None
   
#    print(f"Total number of valid proxies:{len(valid_proxies)}")
   
#    print("Starting scraping")
#    # content = await fetch(session, url)
#    tasks = [fetch(url, random.choice(valid_proxies)) for _ in range(5)]
#    results = await asyncio.gather(*tasks)
#    # soup = BeautifulSoup(content, 'html5lib')
#    # print(soup)
#    print("Scraping results")
#    for result in results:
#       if result:
#          print(result)
      
      
# asyncio.run(main())

semaphore = asyncio.Semaphore(10)
HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

async def filter_proxy(proxy):
    """Filter hanya proxy yang bisa akses DexScreener"""
    target_url = 'https://dexscreener.com'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_url, proxy=proxy, timeout=5, ssl=False) as response:
                if response.status == 200:
                    print(f"✅ Proxy OK: {proxy}")
                    return proxy
                else:
                    print(f"⚠️ Proxy {proxy} gagal dengan status: {response.status}")
    except Exception as e:
        print(f"❌ Proxy {proxy} error: {e}")
    return None

async def fetch(url, proxy):
    """Scrape data menggunakan proxy yang valid"""
    async with semaphore:
        try:
            async with aiohttp.ClientSession(headers=HEADER) as session:
                async with session.get(url, proxy=proxy, timeout=10, ssl=False) as response:
                    if response.status == 200:
                        print(f"✅ Sukses scrape dengan proxy: {proxy}")
                        return await response.text()
                    else:
                        print(f"⚠️ Gagal scrape, status {response.status} dengan proxy: {proxy}")
                        return None
        except Exception as e:
            print(f"⚠️ Proxy {proxy} gagal saat fetch: {e}")
            return None

async def main():
    url = 'https://dexscreener.com/solana/5naj2assh2tnjvzuxwzrqhqwovnuawkj1jzaiafsvg95'

    print("🔍 Menyaring proxy...")
    valid_proxies = await asyncio.gather(*(filter_proxy(proxy) for proxy in proxy_list))
    valid_proxies = [proxy for proxy in valid_proxies if proxy]

    if not valid_proxies:
        print("❌ Tidak ada proxy yang valid!")
        return None
    
    print(f"✅ Total proxy valid: {len(valid_proxies)}")

    print("🚀 Memulai scraping...")
    tasks = [fetch(url, random.choice(valid_proxies)) for _ in range(5)]
    results = await asyncio.gather(*tasks)

    print("📌 Hasil scraping:")
    for i, result in enumerate(results):
        if result:
            print(f"🔹 Result {i+1} (potongan awal):\n{result[:500]}\n")  # Tampilkan 500 karakter pertama

asyncio.run(main())
