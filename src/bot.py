import discord
import asyncio
import shlex
import sys

import config
import commands
from core.database import create_db_tables
from helpers.cmd import *

client = discord.Client()
prefix = config.prefix
create_db_tables() # TODO probably won't stay in this file

async def process_message(msg):
    # If message doesn't start with bot prefix, stop here
    if not (msg.content).startswith(prefix):
        return

    # Split message by spaces
    # TODO CURRENTLY SPLITS ARGS EVEN FOR COMMANDS THAT ONLY TAKE ONE ARG WHICH
    #      MAY HAVE SPACES (e.g. addkek).  EVEN WHEN REJOINING THE ARGS SHLEX
    #      REMOVES ANY QUOTATION MARKS.  FIX THIS.  (probably make a more robust
    #      system that only splits the args in the first place if the command
    #      takes multiple args?)
    msgArr = shlex.split(msg.content)
    # Separate command and args
    cmdText = msgArr[0][len(prefix):].lower()
    args = msgArr[1:] if len(msgArr) > 1 else []

    if not (cmdText in command_names):
        return

    # Proceed to process command

    c = get_command_instance_by_name(cmdText, client)
    if bool(c):         # Ensures c actually exists
        if not c.check_privs(msg.author):
            await client.send_message(msg.channel, "Insufficient Privileges")
        else:
            await c.execute(msg, args)

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="Online"))
    print("Connected Successfully")

@client.event
async def on_message(msg):
    await process_message(msg)

client.run(config.token)
