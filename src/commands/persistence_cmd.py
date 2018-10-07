import requests
from abc import ABC, abstractmethod
from discord import MessageType
from io import BytesIO

import config
import core.database as database
import templates as t
from core.command import *

# Parent class for all !add commands
class AddCommand(Command, ABC):

    @abstractmethod
    def _is_valid_submission(self, msg):
        pass

    @abstractmethod
    def _submit_to_database(self, msg):
        pass

    @abstractmethod
    async def _display_submission(self, msg):
        pass

    # All !add commands require admin privileges
    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        channel = msg.channel

        # Ask user to send new submission

        await self.client.send_typing(channel)
        awaiting_message = await self.client.send_message(channel,
            f"{msg.author.mention} {t.await_submission_message}"
        )

        # Wait for next message from user (with a timeout period set in config)

        response = await self.client.wait_for_message(
            timeout = config.add_row_timeout,
            channel = msg.channel,
            author = msg.author
        )

        if response == None:
            # If no message was sent before timeout ended, abort
            await self.client.send_typing(channel)
            await self.client.send_message(channel, f"{msg.author.mention} {t.add_cancelled_message}")
            return
        elif response.content.lower() == "stop":
            # If user sent 'stop', exit
            await self.client.send_typing(channel)
            await self.client.send_message(channel, t.add_stopped_message)
            return

        # Verify submission is valid for submission type

        if not self._is_valid_submission(response):
            # If what they submitted isn't valid, such as submitting an image
            #    for 'advice', text for 'gif', etc., exit
            await self.client.send_typing(channel)
            await self.client.send_message(channel, t.invalid_submission_message)
            return

        # If database submission double-confirmation is turned on...
        if config.confirm_database_submissions:
            # Verify with user this is what they want to submit
            repost = await self._display_submission(response)
            await self.client.send_typing(channel)
            confirmation = await self.client.send_message(channel,
                f"{msg.author.mention} {t.confirm_submission_message}"
            )

            # Create reaction options
            await self.client.add_reaction(confirmation, t.yes_emoji)
            await self.client.add_reaction(confirmation, t.no_emoji)

            # Wait for user to select one
            res = await self.client.wait_for_reaction(
                message = confirmation,
                emoji = [t.yes_emoji, t.no_emoji],
                user = msg.author,
                timeout = config.confirm_reaction_timeout
            )

            if res == None:
                await self.client.delete_message(repost)
                await self.client.clear_reactions(confirmation)
                await self.client.send_message(channel, f"{msg.author.mention} {t.confirm_reaction_timeout_message}")
                return

            if res.reaction.emoji == t.yes_emoji:
                await self.client.delete_message(repost)
                try:
                    await self.client.clear_reactions(confirmation)
                except:
                    pass
                await self.client.edit_message(confirmation, t.pending_submission_message)
            elif res.reaction.emoji == t.no_emoji:
                await self.client.delete_message(repost)
                try:
                    await self.client.clear_reactions(confirmation)
                except:
                    pass
                await self.client.edit_message(confirmation, t.submission_cancelled_message)
                return
            else:
                await self.client.send_typing(channel)
                await self.client.send_message(channel, t.try_again_message)
                return

        send = t.submission_complete_message
        try:
            # Try adding submission to database
            self._submit_to_database(response)
        except:
            # If it failed, say so
            send = t.submission_failed_message

        try:
            await self.client.edit_message(confirmation, send)
        except:
            # If confirmation is turned off, a new message will need to be
            #    sent instead of editing the old one
            await self.client.send_message(msg.channel, send)

@command
class AddAdviceCommand(AddCommand):
    name = "addadvice"
    description = "Add a piece of advice to the database.  Text only."
    usage = f"`{config.prefix}addadvice`"

    def _is_valid_submission(self, msg):
        return msg.type == MessageType.default and len(msg.content) > 0

    def _submit_to_database(self, msg):
        database.add_advice(msg.author, msg.content)

    async def _display_submission(self, msg):
        return await self.client.send_message(msg.channel, msg.content)

@command
class AddGifCommand(AddCommand):
    name = "addgif"
    description = "Add a gif to the database.  Images only."
    usage = f"`{config.prefix}addgif`"

    def _is_valid_submission(self, msg):
        try:
            # Make sure submission includes an image
            url = msg.attachments[0]['url']
        except:
            return False
        return True

    def _submit_to_database(self, msg):
        url = msg.attachments[0]['url']
        database.add_gif(msg.author, url)

    async def _display_submission(self, msg):
        url = msg.attachments[0]['url']
        img = requests.get(url).content
        return await self.client.send_file(msg.channel, BytesIO(img), filename="gif.gif")

@command
class AddKekCommand(AddCommand):
    name = "addkek"
    description = "Add a kek quote to the database.  Text only."
    usage = f"`{config.prefix}addkek`"

    def _is_valid_submission(self, msg):
        return msg.type == MessageType.default and len(msg.content) > 0

    def _submit_to_database(self, msg):
        database.add_kek(msg.author, msg.content)

    async def _display_submission(self, msg):
        return await self.client.send_message(msg.channel, msg.content)

@command
class AddMemeCommand(AddCommand):
    name = "addmeme"
    description = "Add a meme image to the database.  Images only."
    usage = f"`{config.prefix}addmeme`"

    def _is_valid_submission(self, msg):
        try:
            # Make sure submission includes an image
            url = msg.attachments[0]['url']
        except:
            return False
        return True

    def _submit_to_database(self, msg):
        url = msg.attachments[0]['url']
        database.add_meme(msg.author, url)

    async def _display_submission(self, msg):
        url = msg.attachments[0]['url']
        img = requests.get(url).content
        return await self.client.send_file(msg.channel, BytesIO(img), filename="meme.png")

@command
class AddTrumpCommand(AddCommand):
    name = "addtrump"
    description = "Add a Trump quote to the database.  Text only."
    usage = f"`{config.prefix}addtrump`"

    def _is_valid_submission(self, msg):
        return msg.type == MessageType.default and len(msg.content) > 0

    def _submit_to_database(self, msg):
        database.add_trump(msg.author, msg.content)

    async def _display_submission(self, msg):
        return await self.client.send_message(msg.channel, msg.content)
