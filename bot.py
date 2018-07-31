import discord
import asyncio
import shlex

import config
from commands import PingCommand

client = discord.Client()
prefix = config.prefix

commands = ["ping"] # TODO temporary

async def process_message(msg):
    # If message doesn't start with bot prefix, stop here
    if not (msg.content).startswith(prefix):
        return

    # Split message by spaces
    msgArr = shlex.split(msg.content)
    # Separate command and args
    cmdText = msgArr[0][len(prefix):]
    args = msgArr[1:] if len(msgArr) > 1 else []

    if not (cmdText in commands):
        return

    # TODO temporary
    c = PingCommand(client)
    args = {
        "channel": msg.channel
    }
    await c.execute(args)

    # TODO continue here

@client.event
async def on_ready():
    print("Connected Successfully")

@client.event
async def on_message(msg):
    await process_message(msg)

client.run(config.token)
