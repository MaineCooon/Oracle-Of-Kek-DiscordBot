from core.command import *

from helpers.cmd import command_list, command_names, get_command_by_name

import core.database as database # TODO probably remove (or make more specific) later
import templates

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
        for c in command_list:
            if c.check_privs(c, msg.author):
                arr.append(c.name)
        arr = sorted(arr)
        send = ", ".join(arr)
        await self.client.send_message(msg.channel, send)

# TODO also a temporary command for testing, it makes the user who sent
#      the message an 'Admin' in the Admin table
@command
class AddAdminCommand(Command):
    name = "addadmin"
    description = "why did I make descriptions mandatory"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        new_admin = msg.author

        # If they mentioned a channel, set welcome channel to that
        if len(args) > 0:
            for m in msg.server.members:
                if args[0] == m.mention:
                    new_admin = m
                    break

        database.make_admin(new_admin)
        await self.client.send_message(msg.channel, templates.admin_added_message \
            .format(username_tag=new_admin.mention))


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

@command
class SetWelcomeChannel(Command):
    name = "setwelcomechannel"
    description = "Set welcome channel to this channel."

    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        welcome_channel = msg.channel

        # If they mentioned a channel, set welcome channel to that
        if len(args) > 0:
            for c in msg.server.channels:
                if args[0] == c.mention:
                    welcome_channel = c
                    break

        database.set_welcome_channel(welcome_channel)
        await self.client.send_message(msg.channel, "Welcome channel set!")

@command
class SetPollChannel(Command):
    name = "setpollchannel"
    description = "Set poll channel to this channel."

    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        poll_channel = msg.channel

        # If they mentioned a channel, set poll channel to that
        if len(args) > 0:
            for c in msg.server.channels:
                if args[0] == c.mention:
                    poll_channel = c
                    break

        database.set_poll_channel(poll_channel)
        await self.client.send_message(msg.channel, "Poll channel set!")
