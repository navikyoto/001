import re
import asyncio
from typing import List, Any
from collections import defaultdict
from .scrape import BaseScraper


class Detections(BaseScraper):
    def __init__(self, address: str):
        self.page = 1
        self.address = address
        self.pages_: List[int] = []
        self.url: str = self._url()
        self.holder: defaultdict = defaultdict(str)

    def _url(self) -> str:
        return f'https://etherscan.io/token/generic-tokenholders2?m=light&a={self.address}&s=100000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p={self.page}'


    async def return_(self, content: str, element: str) -> None:
        page = await self.main(content, text_, headers=self.header())
        return await self.scrape_info_(page, element)

    @property
    async def get_url(self) -> None:
        return await self.main(self.url, self.text_)

    async def scrape_page(self) -> None:
        pages = await self.scrape_info_(await self.get_url, 'span.page-link.text-nowrap')
        print(pages)
        page = [re.findall(r'[0-9]+', page.text) for page in pages]
        self.pages_.append(int(page[0][1]))

    async def scrape_info(self) -> None:
        await self.scrape_page()
        result = {}
        for page_number in range(self.pages_[0]):
            self.page = page_number+1
            self.url = self._url()
            task = [
                self.return_(self.url, '.d-flex.align-items-center.gap-1'),
                self.return_(
                    self.url, 'tbody.align-middle.text-nowrap .progress-bar.bg-primary')
            ]

            holders, percentages = await asyncio.gather(*task)

            holder = [str(holder.text).strip() for holder in holders]

            result.update({
                self.soup(str(holder)).text: str(percent['aria-valuenow'])
                for holder, percent in zip(holder, percentages)
            })

            self.holder = result
            ...

        return self.holder

    def run(self) -> Any:
        return asyncio.run(self.scrape_page())
