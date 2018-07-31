from abc import ABC, abstractmethod

# Abstract parent class for all commands
class Command(ABC):
    def __init__(self, client, command_name, cmd_text, description):
        self.client = client
        self.name = command_name
        self.cmd_text = cmd_text
        self.description = description

    @abstractmethod
    async def execute(self, args):
        pass

class PingCommand(Command):
    def __init__(self, client):
        name = "Ping"
        command = "ping"
        description = "Ping pong!"
        super().__init__(client, name, command, description)

    # Args needed:
    # - channel
    async def execute(self, args):
        await self.client.send_message(args["channel"], "Pong!")
