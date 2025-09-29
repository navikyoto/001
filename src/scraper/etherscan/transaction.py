import os, re
from typing import Any
from dataclasses import dataclass

import httpx, asyncio
from bs4 import BeautifulSoup
from selectolax.lexbor import LexborHTMLParser


from scraper import BaseScraper
from ..bscscan.url_ import UrlManager


class Transaction(BaseScraper):
    def __init__(self, address, use_proxies = False ,logger_name = "etherscan.io"):
        super().__init__(logger_name)
        self.address = address

    def _text(self, tx):
        return tx.text()

    def _get_attr(self, tx, element, attr):
        for tx in tx.css(element):
            return tx.attributes.get(attr)

    def test(self, tx, element, return_type):
        match return_type:
            case 1:
                return self._get_attr(tx, element, 'data-title')
            case 0:
                for tx in tx.css(element):
                    return self._text(tx)

    def trans(self):

        url = httpx.get("https://etherscan.io/token/generic-tokentxns2?m=light&contractAddress=0x95AF4aF910c28E8EcE4512BFE46F1F33687424ce&a=&sid=d34c6ab0df45b3ba56310cc56ac29d27&p=1",  headers=self.get_header())
        tx = LexborHTMLParser(url.content)

        # self.test(tx, "tbody.align-middle.text-nowrap tr td:nth-child(2)", 0)
        self.test(tx, "body.align-middle.text-nowrap tr td:nth-child(3) span", 1)

        # Transaction Hash
        # for tx in tx.css('tbody.align-middle.text-nowrap tr td:nth-child(2)'):
        #     print(tx.text()) 

        # Method
        # for tx in tx.css('tbody.align-middle.text-nowrap tr td:nth-child(3) span'):
            # print(tx.attributes.get('data-title'))

        # Age
        # for tx in tx.css('tbody.align-middle.text-nowrap tr td.showAge'):
            # print(tx.text())

        # From
        # for tx in tx.css('tbody.align-middle.text-nowrap tr td:nth-child(9) .js-clipboard.link-secondary'):
            # print(tx.attributes.get('data-clipboard-text'))

        # To
        # for tx in tx.css('tbody.align-middle.text-nowrap tr td:nth-child(11) .js-clipboard.link-secondary'):
        #     print(tx.attributes.get('data-clipboard-text'))

        # Amount
        # for tx in tx.css('tbody.align-middle.text-nowrap tr td:nth-child(12)'):
            # print(tx.text())
        

if __name__ == "__main__":
    address = "0x95AF4aF910c28E8EcE4512BFE46F1F33687424ce"
    tx = Transaction(address)
    print(tx.trans())



