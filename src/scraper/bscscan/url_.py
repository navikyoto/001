from urllib.parse import urlencode

class UrlManager:
   def __init__(self, address, page = 1):
      self.address = address
      self.page = page
      
   def construct_url(self):
      base = "https://bscscan.com/token"
      
      tokenomics_url = f"{base}/{self.address}"
      
      holder_path = f"{base}/generic-tokenholders2?"
      holder_params = {
         "m": "light",
         "a": self.address,
         "s": "1000000000000000000000000000",
         "sid": "70069bba651b7c2c32ee067cd0ed8821",
         "p": self.page
      }
      
      holder_url = f"{holder_path}{urlencode(holder_params)}"
      
      return {
         "base": base,
         "tokenomics": tokenomics_url,
         "holder": holder_url
      }
      