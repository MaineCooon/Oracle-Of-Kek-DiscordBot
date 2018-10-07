import templates as t
from config import prefix
from core.command import *
from core.kekcoin import KekCoin

kekcoin = KekCoin()

@command
class BlockchainCommand(Command):
    name = "blockchain"
    description = "Displays blockchain data."
    usage = f"`{prefix}blockchain`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            result = kekcoin.blockchain
            send = t.display_blockchain_message.format(
                block_count     = "{0:,g}".format(result['block_count']),
                staking_weight  = result['staking_weight'],
                staking_reward  = result['staking_reward'],
                difficulty      = "{0:.8f}".format(result['difficulty']),
                blockchain_size = result['blockchain_size']
            )
        except:
            send = t.blockchain_unavailable_message

        await self.client.send_message(msg.channel, send)

@command
class McapCommand(Command):
    name = "mcap"
    description = "Displays mcap data."
    usage = f"`{prefix}mcap`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            result = kekcoin.mcap
            send = t.display_mcap_message.format(
                mcap_usd = "{0:,.2f}".format(result['mcap_usd']),
                mcap_btc = "{0:.2f}".format(result['mcap_btc']),
                position = "{0:g}".format(result['position'])
            )
        except:
            send = t.mcap_unavailable_message

        await self.client.send_message(msg.channel, send)

@command
class PriceCommand(Command):
    name = "price"
    description = "Displays price data."
    usage = f"`{prefix}price`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            result = kekcoin.price
            send = t.display_price_message.format(
                btc_price  = "{0:.8f}".format(result['price_btc']),
                usd_price  = "{0:.2f}".format(result['price_usd']),
                volume     = "{0:.2f}".format(result['volume']),
                low_24h    = "{0:.8f}".format(result['low_24h']),
                high_24h   = "{0:.8f}".format(result['high_24h']),
                change_24h = "{0:.2f}".format(result['change_24h'])
            )
        except:
            send = t.price_unavailable_message

        await self.client.send_message(msg.channel, send)

@command
class SupplyCommand(Command):
    name = "supply"
    description = "Displays current supply."
    usage = f"`{prefix}supply`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            result = kekcoin.supply
            supply = "{:,}".format(result)
            send = t.display_supply_message.format(supply=supply)
        except:
            send = t.supply_unavailable_message

        await self.client.send_message(msg.channel, send)
