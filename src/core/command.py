from abc import ABC, abstractmethod

from helpers.cmd import register_command

def command(cmd):
    register_command(cmd)
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

    # Returns True if command is usable in this channel, False if not
    # Used mainly for commands only usable in servers or in DMs.  Must be
    #    specifically implemented for command classes that have channel requirements
    def check_channel_type(self, channel):
        return True

    @abstractmethod
    async def execute(self, msg, args):
        pass
