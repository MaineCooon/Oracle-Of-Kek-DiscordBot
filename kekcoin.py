import ccxt

cryptopia = ccxt.cryptopia()
cmc = ccxt.coinmarketcap()

symbol = 'KEK/BTC'

def get_supply():
    result = cmc.fetch_ticker(symbol)['info']['total_supply']
    supply = int(float(result))
    return supply
