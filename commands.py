from abc import ABC, abstractmethod

import database # TODO probably remove (or make more specific) later

command_list = []
command_names = []

def get_command_instance_by_name(command_name, client):
    command_name = command_name.lower()
    for c in command_list:
        if command_name == c.name:
            return c(client)
    return False

def get_command_by_name(command_name):
    command_name = command_name.lower()
    for c in command_list:
        if command_name == c.name:
            return c
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

    # Returns True if user has the privileges for this command, False if not
    # Must be specifically implemented for command classes that have privilege requirements
    def check_privs(self, discord_user):
        return True

    @abstractmethod
    async def execute(self, msg, args):
        pass

@command
class HelpCommand(Command):
    name = "help"
    description = "help command"

    # TODO check if you even need these constructors on all these child classes
    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        if len(args) != 1 or not args[0].lower() in command_names:
            await self.client.send_message(msg.channel, "Must provide one existent command")
            return
        cmd = get_command_by_name(args[0])
        await self.client.send_message(msg.channel, cmd.description)

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
class DemoteAdminCommand(Command):
    name = "demoteadmin"
    description = "demote admin"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        database.remove_admin(msg.author)

# TODO temporary
@command
class AddUserCommand(Command):
    name = "adduser"
    description = "seriously why"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        database.add_user(msg.author)

# TODO temporary
@command
class IsAdminCommand(Command):
    name = "isadmin"
    description = "debug command"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, msg, args):
        await self.client.send_message(msg.channel, database.is_admin(msg.author))

# TODO probably needs cleanup later
@command
class AddKekCommand(Command):
    name = "addkek"
    description = "add kek quote"

    def __init__(self, client):
        super().__init__(client)

    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        if len(args) < 1:
            await self.client.send_message(msg.channel, "Must have args")
            return

        submission = " ".join(args)
        database.add_kek(msg.author, submission)
        await self.client.send_message(msg.channel, "Added!")

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
