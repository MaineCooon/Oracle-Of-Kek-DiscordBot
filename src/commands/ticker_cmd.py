from core.command import *

import core.kekcoin as kekcoin
import templates

@command
class SupplyCommand(Command):
    name = "supply"
    description = "asidjfosidf"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)
        result = kekcoin.get_supply() # TODO error checking etc
        supply = "{:,}".format(result)
        send = templates.display_supply_message.format(supply=supply)
        await self.client.send_message(msg.channel, send)

@command
class PriceCommand(Command):
    name = "price"
    description = "asjdfo"

    async def execute(self, msg, args):
        pass
