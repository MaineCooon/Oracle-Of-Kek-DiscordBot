from abc import ABC, abstractmethod

commands = []

def command(cmd):
    print(cmd.name) # TODO remove
    commands.append(cmd.name)
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
    async def execute(self, args):
        pass

    @classmethod
    def getCommandInstanceByName(command_name):
        pass # TODO

@command
class PingCommand(Command):
    name = "ping"
    description = "Ping pong!"

    def __init__(self, client):
        super().__init__(client)

    # Args needed:
    # - channel
    async def execute(self, args):
        await self.client.send_message(args["channel"], "Pong!")

@command
class DonateCommand(Command):
    name = "donate"
    description = "DONATE DESCRIPTION"

    def __init__(self, client):
        super().__init__(client)

    # Requires args:
    # - msg
    async def execute(self, args):
        await self.client.send_typing(args["msg"].channel)
        await self.client.send_message(args["msg"].channel, "YEET")

@command
class CommandsCommand(Command):
    name = "commands"
    description = "LIST COMMANDS"

    def __init__(self, client):
        super().__init__(client)

    async def execute(self, args):
        string = ", ".join(commands)
        await self.client.send_message(args["msg"].channel, string)
