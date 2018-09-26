from core.command import *

@command
class DonateCommand(Command):
    name = "donate"
    description = "DONATE DESCRIPTION"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)
        await self.client.send_message(msg.channel, "YEET") # TODO fix this
