from urllib.parse import urlencode

class UrlManager:
   def __init__(self, address, page = 1):
      self.address = address
      self.page = page
      
   def construct_url(self):
      base = "https://solscan.io/token/"
      
      tokenomics_url = f"{base}/{self.address}"
      
      holder_params = {
         "page": self.page,
      }
      
      holder_url = f"{base}{self.address}?{urlencode(holder_params)}#holders"
      
      return {
         "base": base,
         "tokenomics": tokenomics_url,
         "holder": holder_url
      }
