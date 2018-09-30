import random
import requests
from io import BytesIO

import templates
from core.command import *
from core.database import get_memes, get_keks, get_gifs, get_trumps, get_advices

@command
class MemeCommand(Command):
    name = "meme"
    description = "meme command"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            # Get random image url from database
            url = random.choice(get_memes()).img_url
        except:
            await self.client.send_message(msg.channel, templates.no_memes_saved_message)
            return

        try:
            # Fetch image from url
            img = requests.get(url).content
            # Send image
            await self.client.send_file(msg.channel, BytesIO(img), filename="meme.png")
        except:
            await self.client.send_message(msg.channel, templates.content_not_loaded_message)

@command
class KekCommand(Command):
    name = "kek"
    description = "kek command"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            kek = random.choice(get_keks()).submission
        except:
            await self.client.send_message(msg.channel, templates.no_keks_saved_message)
            return

        try:
            await self.client.send_message(msg.channel, kek)
        except:
            await self.client.send_message(msg.channel, templates.content_not_loaded_message)

@command
class GifCommand(Command):
    name = "gif"
    description = "gif command"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            # Get random image url from database
            url = random.choice(get_gifs()).img_url
        except:
            await self.client.send_message(msg.channel, templates.no_gifs_saved_message)
            return

        try:
            # Fetch image from url
            img = requests.get(url).content
            # Send image
            await self.client.send_file(msg.channel, BytesIO(img), filename="gif.gif")
        except:
            await self.client.send_message(msg.channel, templates.content_not_loaded_message)

@command
class TrumpCommand(Command):
    name = "trump"
    description = "trump command"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            trump = random.choice(get_trumps()).submission
        except:
            await self.client.send_message(msg.channel, templates.no_trumps_saved_message)
            return

        try:
            await self.client.send_message(msg.channel, trump)
        except:
            await self.client.send_message(msg.channel, templates.content_not_loaded_message)

@command
class AdviceCommand(Command):
    name = "advice"
    description = "advice command"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        try:
            advice = random.choice(get_advices()).submission
        except:
            await self.client.send_message(msg.channel, templates.no_advice_saved_message)
            return

        try:
            await self.client.send_message(msg.channel, advice)
        except:
            await self.client.send_message(msg.channel, templates.content_not_loaded_message)
