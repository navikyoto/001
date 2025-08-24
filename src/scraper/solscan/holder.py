import re
from collections import defaultdict

import asyncio, pandas
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# base_scraper and url_manager from own lib
from scraper import BaseScraper
from .url_ import UrlManager

# Renew the cookies through header.json for etherscan before running the script!
class SolScan(BaseScraper):

    """
    Solscan using asyncronous playwright

        Attributes:
            Address: Meme coin SLP (Solana) based address.
            use_proxies: If True, use proxy for requests (default: False) currently not working.
            logger_name: logger name, for addresing error.
    """

    def __init__(self, use_proxies=False, logger_name="solscan.io"):
        super().__init__(logger_name)
        self.page = 1
        self.address = address
        self.url = self._url()
        self.token_name = None
        self.holder: defaultdict = defaultdict(str)

    def _url(self):
        url = UrlManager(self.address, self.page)
        return url.construct_url()["holder"]

    async def scrape_page(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()

            await page.set_extra_http_headers(self.get_header())
            await page.goto(self.url, wait_until='networkidle')
            await page.wait_for_load_state('networkidle')
            buttons = page.locator("button").nth(40)
            # await buttons.highlight()
            # count = await buttons.count()

            # for i in range(count):
            #     button = buttons.nth(i)
            #     await button.highlight()
            #     print(f"higtlight button {i}")
            #     await asyncio.sleep(1)
  
            # input("press anything to end.....")

            all_data = []
            while True:
                
                await buttons.click()
                await page.wait_for_timeout(3000)
                await page.wait_for_load_state('networkidle')

                content = await page.content()
                soup = BeautifulSoup(content, 'html5lib')

                # First check if button is disabled
                is_disabled = await buttons.is_disabled()
                if is_disabled:
                    print("Reached last page - button is disabled")
                    break

                names = soup.select('.truncateWrapper span.text-neutral6')
                account = soup.select("table tr td:nth-of-type(2) a")
                token_acc = soup.select("table tr td:nth-of-type(3) a")
                quantity = soup.select("table tr td:nth-of-type(4)")
                percentage = soup.select("table tr td:nth-of-type(5)")
                value = soup.select("table tr td:nth-of-type(6)")
                
                def clean(func): return re.sub(
                    r'^/account/', '', func["href"]) 

                for acc, token, qty, perc, val in zip(account,token_acc,quantity,percentage,value):
                    data = {
                       "account": clean(acc),
                       "token_account": clean(token),
                       "quantity": qty.get_text(strip=True),
                       "percetange": perc.get_text(strip=True),
                       "value": val.get_text(strip=True)
                    }

                    # print(data)

                    all_data.append(data)


                # # Click next page button and wait for navigation
           
                # df = pandas.DataFrame(all_data)
                # df.to_csv(f"../src/result/{names[0].get_text(strip=True)}.csv")
                
                df = pandas.DataFrame(all_data)
                df.to_csv(f"../src/result/{names[0].get_text(strip=True)}.csv")
 
if __name__ == "__main__":
    address = "DrZ26cKJDksVRWib3DVVsjo9eeXccc7hKhDJviiYEEZY"
    solscan = SolScan()
    asyncio.run(solscan.scrape_page())
