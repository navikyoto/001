from dataclasses import dataclass
from ..unused_script.scrape import BaseScraper
from typing import List, Dict, Optional, Callable

@dataclass
class Info:
    chainID: str
    tokenAddress: str
    
@dataclass 
class TokenInfo:
    name: str
    contract: str
    network: str
    volume_24: float
    liquidity: float
    market_cap: Optional[float]

def link(info: Info):
    link: str = f"https://api.dexscreener.com/token-pairs/v1/{info.chainID}/{info.tokenAddress}"
    ...
    return link

scraper = BaseScraper()

def get_info( content: List[str]) -> Dict[str, any]:
    for item in content:
        return TokenInfo (
            name = item["baseToken"]["name"],
            contract = item["baseToken"]["address"],
            network = item["chainId"],
            volume_24 = item["volume"]["h24"],
            liquidity = item["liquidity"]["usd"],
            market_cap = item["marketCap"],
        )
    ...

def display_info(info: Callable[[any], any]) -> str:
    print(info)
    ...
    
    
async def info_(info: Info) -> None:
    content = await scraper.main(url = link(info), output = scraper.json_)
    display_info(get_info(content))