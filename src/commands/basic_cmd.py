from core.command import *

from helpers.cmd import command_names, get_command_by_name

import core.database as database # TODO probably remove (or make more specific) later

@command
class HelpCommand(Command):
    name = "help"
    description = "help command"

    async def execute(self, msg, args):
        if len(args) != 1 or not args[0].lower() in command_names:
            await self.client.send_message(msg.channel, "Must provide one existent command")
            return
        cmd = get_command_by_name(args[0])
        await self.client.send_message(msg.channel, cmd.description)

@command
class PingCommand(Command):
    name = "ping"
    description = "Ping pong!"

    async def execute(self, msg, args):
        await self.client.send_message(msg.channel, "Pong!")

@command
class CommandsCommand(Command):
    name = "commands"
    description = "LIST COMMANDS"

    async def execute(self, msg, args):
        arr = []
        for c in command_names:
            arr.append(c)
        string = ", ".join(arr)
        await self.client.send_message(msg.channel, string)

# TODO also a temporary command for testing, it makes the user who sent
#      the message an 'Admin' in the Admin table
@command
class AddAdminCommand(Command):
    name = "addadmin"
    description = "why did I make descriptions mandatory"

    async def execute(self, msg, args):
        # TODO run check on if they're already an admin and if so tell them no
        database.make_admin(msg.author)

# TODO temporary
@command
class DemoteAdminCommand(Command):
    name = "demoteadmin"
    description = "demote admin"

    async def execute(self, msg, args):
        database.remove_admin(msg.author)

# TODO temporary
@command
class AddUserCommand(Command):
    name = "adduser"
    description = "seriously why"

    async def execute(self, msg, args):
        database.add_user(msg.author)

# TODO temporary
@command
class IsAdminCommand(Command):
    name = "isadmin"
    description = "debug command"

    async def execute(self, msg, args):
        await self.client.send_message(msg.channel, database.is_admin(msg.author))
