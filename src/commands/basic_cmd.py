from discord import Embed

import templates as t
import core.database as db
from config import prefix
from core.command import *

@command
class CommandsCommand(Command):
    name = "commands"
    description = "Lists all commands available in the current context."
    usage = f"`{prefix}commands`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)
        arr = []
        for c in command_list:
            if c.check_privs(c, msg.author) and c.check_channel_type(c, msg.channel):
                arr.append(c.name)
        arr = sorted(arr)
        send = ", ".join(arr)
        await self.client.send_message(msg.channel, send)

@command
class HelpCommand(Command):
    name = "help"
    description = "Provides descriptions and usage information for commands.  " \
        "Using the command_name argument will show details about the command of " \
        "that name.  Using no arguments will send a summary of all commands to your DMs."
    usage = f"`{prefix}help <command_name>` or `{prefix}help`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        # Handle if a specific command was provided
        if len(args) == 1:
            cmd = get_command_by_name(args[0])
            if cmd != False:
                await self.client.send_message(msg.channel,
                    t.command_help_message.format(description=cmd.description, usage=cmd.usage)
                )
                return

        # Create the embed list
        # This is kind of hard to parse just trust it
        embeds = []
        embed_string = ''
        commands = sorted(command_list, key=lambda c: c.name)
        for i in range(len(commands)):
            c = commands[i]

            # Don't include commands user doesn't have privileges to
            if not c.check_privs(c, msg.author):
                continue

            entry = t.single_help_description.format(command_name=c.name, command_description=c.description)
            if len(embed_string) + len(entry) < 1024:
                if len(embed_string) > 0:
                    embed_string += '\n'
                embed_string += entry
                if i+1 != len(commands): # If this is the last command, it should jump down to embed
                    continue
            # If about to go over embed limit, put embed in list and empty str
            embed = Embed().add_field(
                name = "Help",
                value = embed_string
            )
            embeds.append(embed)
            if i+1 != len(commands):
                embed_string = entry # Keep current command from getting cut off

        # Send embeds to user's DMs
        try:
            for e in embeds:
                await self.client.send_message(msg.author, embed=e)
        except:
            await self.client.send_message(msg.channel, t.cant_dm_message)
            return

        await self.client.send_message(msg.channel, t.help_sent_message)

@command
class PingCommand(Command):
    name = "ping"
    description = "Ping pong!"
    usage = f"`{prefix}ping`"

    async def execute(self, msg, args):
        await self.client.send_message(msg.channel, "Pong!")

@command
class AddAdminCommand(Command):
    name = "addadmin"
    description = "Add user as an admin on the bot.  May need to be done inside " \
        "a server for @ to work right."
    usage = f"`{prefix}addadmin @<user>`"

    def check_privs(self, discord_user):
        return db.is_admin(discord_user)

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        new_admin = msg.author

        # If they mentioned a user, make them an admin
        if len(args) > 0:
            if len(msg.mentions) != 1:
                await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
                return
            else:
                for m in msg.server.members:
                    if args[0].replace('!', '') == m.mention.replace('!', ''):
                        new_admin = m
                        db.make_admin(new_admin)
                        await self.client.send_message(msg.channel, t.admin_added_message \
                            .format(username_tag=new_admin.mention))
                        return
                await self.client.send_message(msg.channel, t.cant_add_admin_message.format(args[0]))
                return

        await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))

@command
class SetWelcomeChannel(Command):
    name = "setwelcomechannel"
    description = "Set welcome channel to this channel."
    usage = f"`{prefix}setwelcomechannel`"

    def check_privs(self, discord_user):
        return db.is_admin(discord_user)

    def check_channel_type(self, channel):
        return not channel.is_private

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        welcome_channel = msg.channel

        # If they mentioned a channel, set welcome channel to that
        if len(args) > 0:
            for c in msg.server.channels:
                if args[0] == c.mention:
                    welcome_channel = c
                    break

        db.set_welcome_channel(welcome_channel)
        await self.client.send_message(msg.channel, "Welcome channel set!")

@command
class SetPollChannel(Command):
    name = "setpollchannel"
    description = "Set poll channel to this channel."
    usage = f"`{prefix}setpollchannel`"

    def check_privs(self, discord_user):
        return db.is_admin(discord_user)

    def check_channel_type(self, channel):
        return not channel.is_private

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        poll_channel = msg.channel

        # If they mentioned a channel, set poll channel to that
        if len(args) > 0:
            for c in msg.server.channels:
                if args[0] == c.mention:
                    poll_channel = c
                    break

        db.set_poll_channel(poll_channel)
        await self.client.send_message(msg.channel, "Poll channel set!")
