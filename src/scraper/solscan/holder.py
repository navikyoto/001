import re
from collections import defaultdict

import asyncio, pandas
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from scraper import BaseScraper
from .url_ import UrlManager

class SolScan(BaseScraper):
    def __init__(self, use_proxies=False, logger_name="solscan.io"):
        super().__init__(logger_name)
        self.page = 1
        # self.address = address
        # self.url = self._url()
        self.token_name = None
        self.holder: defaultdict = defaultdict(str)

    # def _url(self):
    #     url = UrlManager(self.address, self.page)
    #     return url.construct_url()["holder"]

    async def scrape_page(self):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=False)
            page = await browser.new_page()

            await page.set_extra_http_headers(self.get_header())
            await page.goto("https://solscan.io/token/CpdKgsZMtZ54FK5vbyLq5wNyH2uRmSxi8AtEAADipump?page=98", wait_until='networkidle')
            await page.wait_for_load_state('networkidle')
            # await page.get_by_role("button").nth(36).highlight()
            buttons = page.get_by_role("button").nth(36)
            # await buttons.highlight()
            # count = await buttons.count()

            # for i in range(count):
            #     button = buttons.nth(i)
            #     await button.highlight()
            #     print(f"higtlight button {i}")
            #     await asyncio.sleep(1)
                

            # print(next_button)
            # input("press anything to end.....")
            all_data = []

            while True:
                content = await page.content()
                soup = BeautifulSoup(content, 'html5lib')

                # First check if button is disabled
                is_disabled = await buttons.is_disabled()
                if is_disabled:
                    print("Reached last page - button is disabled")
                    break

                name = soup.select('.truncateWrapper span.text-neutral6')
                account = soup.select("table tr td:nth-of-type(2) a")
                token_acc = soup.select("table tr td:nth-of-type(3) a")
                quantity = soup.select("table tr td:nth-of-type(4)")
                percentage = soup.select("table tr td:nth-of-type(5)")
                value = soup.select("table tr td:nth-of-type(6)")
                
                # print(account, token_acc, quantity, percentage, value)

                def clean(func): return re.sub(
                    r'^/account/', '', func["href"]) 

                name = clean(account)
                print(name)

                for name, acc, token, qty, perc, val in zip(name, account, token_acc, quantity, percentage, value):
                    data = {
                        "account": clean(acc),
                        "token_account": clean(token),
                        "quantity": qty.get_text(strip=True),
                        "percentage": perc.get_text(strip=True),
                        "value": val.get_text(strip=True)
                    }

                    # print(name, acc, token, qty, perc, val)

                #     self.token_name = name.get_text(strip=True)
                #     all_data.append(data)

                # Click next page button and wait for navigation
                await buttons.click()
                await page.wait_for_timeout(10)
                await page.wait_for_load_state('networkidle')
                # df = pandas.DataFrame(all_data, columns=[
                #                       "account", "token_account", "quantity", "percentage", "value"])
                # df.to_csv(f"../src/result/{self.token_name}.csv")
            # print(all_data)
# 
if __name__ == "__main__":
    address = "CpdKgsZMtZ54FK5vbyLq5wNyH2uRmSxi8AtEAADipump"
    solscan = SolScan()
    asyncio.run(solscan.scrape_page())
