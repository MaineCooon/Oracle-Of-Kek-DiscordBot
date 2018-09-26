from core.command import *

import core.database as database
import templates

# TODO probably needs cleanup later
@command
class AddKekCommand(Command):
    name = "addkek"
    description = "add kek quote"

    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        await self.client.send_message(msg.channel, templates.await_kek_message.format(user=msg.author.display_name))
        response = await self.client.wait_for_message(timeout=20, author=msg.author)
        if response == None:
            await self.client.send_message(msg.channel, "Took longer than 20 seconds, cancelled.")
            return
        elif response.content.lower() == "stop":
            await self.client.send_message(msg.channel, "Stopped.  :P")
            return

        database.add_kek(msg.author, response.content)
        await self.client.send_message(msg.channel, "Added kek '{kek}'".format(kek=response.content))
        # if len(args) < 1:
        #     await self.client.send_message(msg.channel, "Must have args")
        #     return
        #
        # submission = " ".join(args)
        # database.add_kek(msg.author, submission)
        # await self.client.send_message(msg.channel, "Added!")
