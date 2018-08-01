from abc import ABC, abstractmethod

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
