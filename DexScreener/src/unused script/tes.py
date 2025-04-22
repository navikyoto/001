# Python3 program to extract all the numbers from a string
# import re

# # Function to extract all the numbers from the given string
# def getNumbers(str):
# 	array = re.findall(r'[0-9]+', str)
# 	return array

# # Driver code
# str = "Page 1 of 4"
# array = getNumbers(str)
# # print(*array)
# tes = int(array[1])

# # for i in range(tes):
# #    print(i+1)
# name = 'tes'   
# txt3 = "My name is {name}, I'm {age}"
# tes = txt3.format(name=name, age='21')

# class satu():
#    def __init__(self, nama):
#       self.name = nama

# class dua(satu):
#    def tes(self):
#       print(self.name)
      
# sat = dua('tes')
# sat.tes()

# class Detections():
#     def __init__(self):
#         self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
#         self.page = []
#         self.url = 'https://etherscan.io/token/generic-tokenholders2?m=light&a={}&s=1000000000000000000000000000&sid=07467e3c4a8cf6bc8d0418bb4ac45e62&p={}'


#     def tes(self):
#         print(self.tokenAddress)

#     async def fetch(self,session, url):
#         async with session.get(url, headers = self.headers) as response:
#             html = await response.text()
#             return html
        

#     async def get_url(self):
#         async with aiohttp.ClientSession() as session:
#             content = await self.fetch(session, self.url.format(self.tokenAddress, 0))
#             soup = BeautifulSoup(content, 'lxml')
#             for page in soup.select('span.page-link.text-nowrap'):
#             array = re.findall(r'[0-9]+', page.text)
#             self.page.append(int(array[1]))
            

#     async def main(self):
#         await self.get_url()
#         for i in range(self.page[0]):
#             async with aiohttp.ClientSession() as session:
#             content = await self.fetch(session, self.url.format(self.tokenAddress, i+1))
#             soup = BeautifulSoup(content, 'lxml')
#             holders = '.d-flex.align-items-center.gap-1'
#             percents = '.progress-bar.bg-primary'
#             for holder,percent in zip(soup.select(holders), soup.select(percents)):
#                 print(f"{holder.text} :{percent['aria-valuenow']:%}")
            
            
#     def get_holder(self):
#         return asyncio.run(self.main())

# from utils.scrape import main, json_, text_
# url = 'https://api.dexscreener.com/token-pairs/v1/ethereum/0x41D06390b935356b46aD6750bdA30148Ad2044A4'

# main(url, json_)
# import csv
# import pandas as pd

# with open('file.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['name', 'age'])
#     writer.writerow(['John Doe', 30])

# pd.read_csv('stocks.csv')

# Output:
# The CSV file named 'file.csv' will be created and two rows of data will be written to it.

from scraper.base_scraper import MainScrape


