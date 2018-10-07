from abc import ABC, abstractmethod
from discord import ChannelType

command_list = []
command_names = []

def register_command(cmd):
    print(f"Loaded Command: {cmd.name}")
    command_list.append(cmd)
    command_names.append(cmd.name.lower())

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

    @property
    @abstractmethod
    def usage(self):
        pass

    # Returns True if user has the privileges for this command, False if not
    # Must be specifically implemented for command classes that have privilege requirements
    def check_privs(self, discord_user):
        return True

    # Returns True if command is usable in this channel, False if not
    # Used mainly for commands only usable in servers or in DMs.  Must be
    #    specifically implemented for command classes that have channel requirements
    def check_channel_type(self, channel):
        return channel.type == ChannelType.text or channel.is_private

    @abstractmethod
    async def execute(self, msg, args):
        pass
