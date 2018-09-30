import ccxt
import requests
from random import randint

from config import cryptopia_api_key

cryptopia = ccxt.cryptopia()
cmc = ccxt.coinmarketcap()
exp_url = "http://explorer.kekcoin.co/api/"

symbol = 'KEK/BTC'

class KekCoin():
    def __init__(self):
        self._cryptopia = ccxt.cryptopia()
        self._cmc = ccxt.coinmarketcap()

        self.symbol = "KEK/BTC"
        print("Initialized KekCoin class")

    @property
    def supply(self):
        result = self._cmc.fetch_ticker(symbol)['info']['total_supply']
        supply = int(float(result))
        return supply

    @property
    def price(self):
        cmc_ticker = self._cmc.fetch_ticker(symbol)
        crypt_ticker = self._cryptopia.fetch_ticker(symbol)

        price_btc = float( cmc_ticker['info']['price_btc'] )
        price_usd = float( cmc_ticker['info']['price_usd'] )
        volume = crypt_ticker['info']['Volume']
        low_24h = crypt_ticker['info']['Low']
        high_24h = crypt_ticker['info']['High']
        change_24h = crypt_ticker['info']['Change']

        # Debug printing
        # print("price_btc:  " + str(price_btc) )
        # print("price_usd:  " + str(price_usd) )
        # print("volume:     " + str(volume) )
        # print("low_24h:    " + str(low_24h) )
        # print("high_24h:   " + str(high_24h) )
        # print("change_24h: " + str(change_24h) )
        #
        # print()
        #
        # print("price_btc:  " + "{0:.8f}".format(price_btc) )
        # print("price_usd:  " + "{0:.2f}".format(price_usd) )
        # print("volume:     " + "{0:.2f}".format(volume) )
        # print("low_24h:    " + "{0:.8f}".format(low_24h) )
        # print("high_24h:   " + "{0:.8f}".format(high_24h) )
        # print("change_24h: " + "{0:.2f}".format(change_24h) )

        price = {
            'price_btc': price_btc,
            'price_usd': price_usd,
            'volume': volume,
            'low_24h': low_24h,
            'high_24h': high_24h,
            'change_24h': change_24h
        }

        return price

    @property
    def blockchain(self):
        block_count = float( requests.get("{}/getblockcount".format(exp_url)).text )
        staking_weight = 'TBA'
        staking_reward = 'TBA'
        difficulty = float( requests.get("{}/getdifficulty".format(exp_url)).text )
        blockchain_size = 'TBA'

        blockchain_info = {
            'block_count': block_count,
            'staking_weight': staking_weight,
            'staking_reward': staking_reward,
            'difficulty': difficulty,
            'blockchain_size': blockchain_size
        }

        return blockchain_info

    @property
    def mcap(self):
        cmc_ticker = self._cmc.fetch_ticker(symbol)

        mcap_usd = float( cmc_ticker['info']['market_cap_usd'] )
        mcap_btc = float( cmc_ticker['info']['market_cap_btc'] )
        position = float( cmc_ticker['info']['rank'] )

        mcap_info = {
            'mcap_usd': mcap_usd,
            'mcap_btc': mcap_btc,
            'position': position
        }

        return mcap_info
