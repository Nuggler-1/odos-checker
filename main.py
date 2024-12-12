from eth_account import Account
from eth_account.messages import encode_defunct
from utils.utils import error_handler, check_proxy, get_proxy, sleep, decimalToInt
from utils.constants import DEFAULT_ADDRESSES
import requests
from fake_useragent import UserAgent
import json
import questionary
from loguru import logger
import sys
from config import DELAY_ACCOUNTS

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> |  <level>{message}</level>",
    colorize=True
)
class Checker(): 

    def __init__(self,address:str, proxy:dict = None): 

        self.address = address
        self.proxy = proxy 
        self.base_url = f'https://api.odos.xyz/loyalty/users/{self.address}/balances'
        self.headers = {
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, br, zstd',
            'accept-language':'en-US;q=0.8,en;q=0.7',
            'origin': 'https://app.odos.xyz',
            'referer': 'https://app.odos.xyz/',
            'user-agent': UserAgent().random
        }
    
    @error_handler('getting amount')
    def get_amount(self, ): 

        response = requests.get(self.base_url, proxies=self.proxy, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f'Error getting amount: {response.status_code}')
        
        amount = decimalToInt(
            int(response.json()['data']['pendingTokenBalance']),
            18
        )
        logger.info(f'{self.address}: {amount}')
        return amount

def main(): 

    check_proxy()

    with open(DEFAULT_ADDRESSES, 'r', encoding='utf-8') as f: 
        addresses = f.read().splitlines()

    total_amount = 0
    for address in addresses: 
        proxy = get_proxy(address)
        checker = Checker(address, proxy)
        amount = checker.get_amount()
        total_amount += amount 
    logger.success(f'Total amount to claim: {total_amount}')


if __name__ == '__main__': 
    main()