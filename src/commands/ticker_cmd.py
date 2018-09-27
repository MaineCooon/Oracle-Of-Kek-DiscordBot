from core.command import *

import core.kekcoin as kekcoin
import templates

from core.kekcoin import KekCoin

kekcoin = KekCoin()

@command
class SupplyCommand(Command):
    name = "supply"
    description = "asidjfosidf"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            result = kekcoin.supply
            supply = "{:,}".format(result)
            send = templates.display_supply_message.format(supply=supply)
        except:
            send = templates.supply_unavailable_message

        await self.client.send_message(msg.channel, send)

@command
class PriceCommand(Command):
    name = "price"
    description = "asjdfo"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            result = kekcoin.price
            send = templates.display_price_message.format(
                btc_price  = "{0:.8f}".format(result['price_btc']),
                usd_price  = "{0:.2f}".format(result['price_usd']),
                volume     = "{0:.2f}".format(result['volume']),
                low_24h    = "{0:.8f}".format(result['low_24h']),
                high_24h   = "{0:.8f}".format(result['high_24h']),
                change_24h = "{0:.2f}".format(result['change_24h'])
            )
        except:
            send = templates.price_unavailable_message

        await self.client.send_message(msg.channel, send)

@command
class BlockchainCommand(Command):
    name = "blockchain"
    description = "blockchain command"

    async def execute(self, msg, args):
        # TODO implement !blockchain
        await self.client.send_message(msg.channel, "Coming soon...")

@command
class McapCommand(Command):
    name = "mcap"
    description = "mcap command"

    async def execute(self, msg, args):
        # TODO implement !mcap
        await self.client.send_message(msg.channel, "Coming soon...")
