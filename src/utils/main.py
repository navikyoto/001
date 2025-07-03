import asyncio
import aiohttp

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'accept-language': "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
    'Cookie': "bscscan_offset_datetime=+7; bscscan_switch_token_amount_value=value; bscscan_cookieconsent=True; ASP.NET_SessionId=2nsms4ipwdn4nd5zuazyyulr; __cflb=0H28vyb6xVveKGjdV3CYUMgiti5JgVsbAPqujG8Lrg4; cf_chl_rc_ni=1; cf_clearance=BjSR9TRq1zzEuqm4FKGViJE7S0vUhTPOIrML7deUOac-1748344684-1.2.1.1-nOv_tcOCy6zJ8SLXgj7ilQD0PNFngzBZij33RD1girIwzwLMWcUbbG1fdG5pL4zTFWtSt8WcrSBcjPophqHJt_Tzy8nsollffhFLSty7DrwYTYsqJXKL4S__Nu.vzeRNB8z6gFh_AmlLys6UBeQFl.HEGbQxMInJMtH5NyVHsR2Uo3cTrZ9KSYxN18nQSa1Y7p5tQDOhbxg9FIjLTQS3_D7CVCcBA3I4fbDP_ONB7T_S7AcsRp3DeDtiN3L.3.64cmCqtqpIN6sk1EH3WEtb1TEv6jHl2UzJdOO2XLgLatrIH6j6x146gqvzZ2kdm7V57Lj34qL6S4B3qxeCzzxnyBUlzfqMU20BfeTJwsxWuip5jP90uRrb7P2TucD1sfYv",
    'dnt': "1",
    'priority': "u=0, i",
    'referer': "https://bscscan.com/token/0xA49fA5E8106E2d6d6a69E78df9B6A20AaB9c4444",
    'sec-ch-ua': "'Chromium';v='136', 'Google Chrome';v='136', 'Not.A/Brand';v='99' ",
    'sec-ch-ua-arch': "'x86'",
    'sec-ch-ua-bitness': "'64'",
    'sec-ch-ua-full-version': "'136.0.7103.114'",
    'sec-ch-ua-full-version-list': "'Chromium';v='136.0.7103.114', 'Google Chrome';v='136.0.7103.114', 'Not.A/Brand';v='99.0.0.0'",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-model': "''",
    'sec-ch-ua-platform': "'Windows'",
    'sec-ch-ua-platform-version': "'19.0.0'",
    'sec-fetch-dest': "iframe",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "same-origin",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

async def fetch(session, url,):
    async with session.get(url, headers=headers) as response:
        return await response.text()
    
async def scraper(url):
    async with aiohttp.ClientSession() as session:
        content = await fetch(session, url)
        return content
    
print(asyncio.run(scraper("https://bscscan.com/token/generic-tokenholders2?m=light&a=0xA49fA5E8106E2d6d6a69E78df9B6A20AaB9c4444&s=1000000000000000000000000000&sid=6ee5ac0d495901a36d8e78708f81ccde&p=1")))