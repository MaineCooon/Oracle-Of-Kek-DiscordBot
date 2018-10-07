import random
import requests
from io import BytesIO

import templates as t
from config import prefix
from core.command import *
from core.database import get_memes, get_keks, get_gifs, get_trumps, get_advices

@command
class AdviceCommand(Command):
    name = "advice"
    description = "Sends a random piece of advice from the bot's database."
    usage = f"`{prefix}advice`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            advice = random.choice(get_advices()).submission
        except:
            await self.client.send_message(msg.channel, t.no_advice_saved_message)
            return

        try:
            await self.client.send_message(msg.channel, advice)
        except:
            await self.client.send_message(msg.channel, t.content_not_loaded_message)

@command
class GifCommand(Command):
    name = "gif"
    description = "Sends a random gif from the bot's database."
    usage = f"`{prefix}gif`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            # Get random image url from database
            url = random.choice(get_gifs()).img_url
        except:
            await self.client.send_message(msg.channel, t.no_gifs_saved_message)
            return

        try:
            # Fetch image from url
            img = requests.get(url).content
            # Send image
            await self.client.send_file(msg.channel, BytesIO(img), filename="gif.gif")
        except:
            await self.client.send_message(msg.channel, t.content_not_loaded_message)

@command
class KekCommand(Command):
    name = "kek"
    description = "Sends a random kek quote from the bot's database."
    usage = f"`{prefix}kek`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            kek = random.choice(get_keks()).submission
        except:
            await self.client.send_message(msg.channel, t.no_keks_saved_message)
            return

        try:
            await self.client.send_message(msg.channel, kek)
        except:
            await self.client.send_message(msg.channel, t.content_not_loaded_message)

@command
class MemeCommand(Command):
    name = "meme"
    description = "Sends a random meme images from the bot's database."
    usage = f"`{prefix}meme`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            # Get random image url from database
            url = random.choice(get_memes()).img_url
        except:
            await self.client.send_message(msg.channel, t.no_memes_saved_message)
            return

        try:
            # Fetch image from url
            img = requests.get(url).content
            # Send image
            await self.client.send_file(msg.channel, BytesIO(img), filename="meme.png")
        except:
            await self.client.send_message(msg.channel, t.content_not_loaded_message)

@command
class TrumpCommand(Command):
    name = "trump"
    description = "Sends a random Trump quote from the bot's database."
    usage = f"`{prefix}trump`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            trump = random.choice(get_trumps()).submission
        except:
            await self.client.send_message(msg.channel, t.no_trumps_saved_message)
            return

        try:
            await self.client.send_message(msg.channel, trump)
        except:
            await self.client.send_message(msg.channel, t.content_not_loaded_message)
