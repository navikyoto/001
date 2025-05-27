from camoufox.sync_api import Camoufox
import requests
from rich import print
import os

class Extractor:
   def __init__(self):
      self.session = requests.Session()
   
   def headers_from_bowser(self, url):
      with Camoufox() as browser:
         page = browser.new_page()
         page.goto("https://www.coinpayu.com/dashboard")
         
         def handle_requests(requests):
            global requests_headers
            if "api" in requests.url:
               requests_headers = requests.headers
               for k, v in requests_headers.items():
                  if k.lower() not in [
                     "content-length",
                     "transfer-encoding",
                     "set-cookie",
                  ]:
                     self.session.headers.update({k, v})
                     
         page.on("request", handle_requests)
         page.goto(url)
         page.wait_for_load_state("networkidle")
         page.reload()
         page.wait_for_load_state("networkidle")
         browser.close()
         print("session headers", self.session.headers)
         
   def get(self, url):
      resp = self.session.get(url)
      return resp