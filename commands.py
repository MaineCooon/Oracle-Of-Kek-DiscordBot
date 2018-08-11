from abc import ABC, abstractmethod

import database # TODO probably remove (or make more specific) later

command_list = []
command_names = []

def get_command_instance_by_name(command_name, client):
    for c in command_list:
        if command_name.lower() == c.name:
            return c(client)
    return False

def command(cmd):
    print(cmd.name) # TODO remove
    command_list.append(cmd)
    command_names.append(cmd.name.lower())
    return cmd

# Abstract parent class for all commands
class Command(ABC):
    def __init__(self, client):
        self.client = client

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    async def execute(self, msg, args):
        pass

# TODO also a temporary command for testing, it makes the user who sent
#      the message an 'Admin' in the Admin table
@command
class AddAdminCommand(Command):
    name = "addadmin"
    description = "why did I make descriptions mandatory"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        # TODO run check on if they're already an admin and if so tell them no
        database.make_admin(msg.author)

# TODO temporary
@command
class AddUserCommand(Command):
    name = "adduser"
    description = "seriously why"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        database.add_user(msg.author)

# # TODO TEMPORARY CLASS FOR TESTING
# @command
# class AddCommand(Command):
#     name = "add"
#     description = "reet"
#
#     def __init__(self, client):
#         super().__init__(client)
#
#     async def execute(self, msg, args):
#         test_function()

@command
class PingCommand(Command):
    name = "ping"
    description = "Ping pong!"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        await self.client.send_message(msg.channel, "Pong!")

@command
class DonateCommand(Command):
    name = "donate"
    description = "DONATE DESCRIPTION"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)
        await self.client.send_message(msg.channel, "YEET")

@command
class CommandsCommand(Command):
    name = "commands"
    description = "LIST COMMANDS"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        arr = []
        for c in command_names:
            arr.append(c)
        string = ", ".join(arr)
        await self.client.send_message(msg.channel, string)
