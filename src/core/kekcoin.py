import ccxt

from random import randint

from config import cryptopia_api_key

cryptopia = ccxt.cryptopia()
cmc = ccxt.coinmarketcap()

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
        return supply # TODO Verify this method still works

    @property
    def price_btc(self):
        pass

    @property
    def price_usd(self):
        pass



def get_supply():
    result = cmc.fetch_ticker(symbol)['info']['total_supply']
    supply = int(float(result))
    return supply

class TestClass():
    def __init__(self, name):
        self.name = name

    @property
    def random_number(self):
        return randint(1, 10)
