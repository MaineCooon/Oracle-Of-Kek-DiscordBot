import templates as t
from config import prefix
from core.command import *

@command
class DonateCommand(Command):
    name = "donate"
    description = "Displays donation information."
    usage = f"`{prefix}donate`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)
        await self.client.send_message(msg.channel, t.donate_message)

@command
class LegalCommand(Command):
    name = "legal"
    description = "Displays legal disclaimer."
    usage = f"`{prefix}legal`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)
        await self.client.send_message(msg.channel, t.legal_message)
