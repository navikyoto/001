from urllib.parse import urlencode

class UrlManager:
   def __init__(self, address, page = 1):
      self.address = address
      self.page = page
      
   def construct_url(self):
      base = "https://etherscan.io/token"
      
      tokenomics_url = f"{base}/{self.address}"
      
      holder_path = f"{base}/generic-tokenholders2?"
      holder_params = {
         "m": "light",
         "a": self.address,
         "s": "100000000000000000000000000",
         "sid": "145bf8274ccc024069bd6b801cc28331",
         "p": self.page
      }
      
      holder_url = f"{holder_path}{urlencode(holder_params)}"
      
      return {
         "base": base,
         "tokenomics": tokenomics_url,
         "holder": holder_url
      }
      